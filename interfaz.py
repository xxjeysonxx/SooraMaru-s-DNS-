# Sooramaru's DNS DS
# Fork of RiiConnect24 DNS Server (based on sudomemoDNS)
# Original authors: Austin Burk / RiiConnect24 team
# Modified with GUI, ConnTest fix, startup delay and logging improvements

from datetime import datetime
import time
import threading
import ctypes

from dnslib import DNSLabel, QTYPE, RD, RR
from dnslib import A, AAAA, CNAME, MX, NS, SOA, TXT
from dnslib.server import DNSServer

import socket
import requests
import json
import sys
import tkinter as tk
from tkinter import scrolledtext, messagebox
from http.server import BaseHTTPRequestHandler, HTTPServer

# ----------------- Utilidades -----------------

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

RIICONNECT24DNSSERVER_VERSION = "1.2"
MY_IP = get_ip()

# ----------------- GUI -----------------

root = tk.Tk()

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
    "sooramaru.dns.server.v1"
)

root.title("Sooramaru's DNS DS - RiiConnect24 Fork")
root.geometry("800x520")
root.configure(bg="black")
root.iconbitmap("icono.ico")

# ❌ Quitar maximizar (solo minimizar)
root.resizable(False, False)

# -------- Layout principal --------

main_frame = tk.Frame(root, bg="black")
main_frame.pack(fill="both", expand=True)

left_frame = tk.Frame(main_frame, bg="black")
left_frame.pack(fill="both", expand=True)

# -------- Labels superiores --------

ip_label = tk.Label(
    left_frame,
    text=f"Primary DNS: {MY_IP}    Secondary DNS: 1.1.1.1",
    font=("Arial", 11),
    bg="black",
    fg="#00ff00"
)
ip_label.pack(pady=5)

credit_label = tk.Label(
    left_frame,
    text="Sooramaru's DNS DS  |  forked from RiiConnect24 (Git)",
    font=("Arial", 10, "italic"),
    bg="black",
    fg="#00ff00"
)
credit_label.pack(pady=2)

# -------- Log estilo terminal --------

log_box = scrolledtext.ScrolledText(
    left_frame,
    state="disabled",
    bg="black",
    fg="#00ff00",
    insertbackground="#00ff00"
)
log_box.pack(fill="both", expand=True, padx=10, pady=10)

def gui_log(text):
    log_box.configure(state="normal")
    log_box.insert("end", f"[{datetime.now().strftime('%H:%M:%S')}] {text}\n")
    log_box.configure(state="disabled")
    log_box.yview("end")

# Mensaje inicial
gui_log("==============================================")
gui_log(" Sooramaru's DNS DS")
gui_log(" forked from RiiConnect24 (Git)")
gui_log("==============================================")

# ----------------- Logger DNS -----------------

class RiiConnect24DNSLogger(object):
    def log_recv(self, handler, data):
        pass
    def log_send(self, handler, data):
        pass
    def log_request(self, handler, request):
        qname = str(request.q.qname)

        # Ocultar spam del conntest
        if "conntest.nintendowifi.net" in qname:
            return

        gui_log("[DNS] Received: " + qname + " from " + handler.client_address[0])

    def log_reply(self, handler, reply):
        pass
    def log_error(self, handler, e):
        gui_log("[ERROR] Invalid DNS request from " + handler.client_address[0])
    def log_truncated(self, handler, reply):
        pass
    def log_data(self, dnsobj):
        pass

# ----------------- Registros DNS -----------------

EPOCH = datetime(1970, 1, 1)
SERIAL = int((datetime.utcnow() - EPOCH).total_seconds())

TYPE_LOOKUP = {
    A: QTYPE.A,
    AAAA: QTYPE.AAAA,
    CNAME: QTYPE.CNAME,
    MX: QTYPE.MX,
    NS: QTYPE.NS,
    SOA: QTYPE.SOA,
    TXT: QTYPE.TXT,
}

class Record:
    def __init__(self, rdata_type, *args, rtype=None, rname=None, ttl=None, **kwargs):
        if isinstance(rdata_type, RD):
            self._rtype = TYPE_LOOKUP[rdata_type.__class__]
            rdata = rdata_type
        else:
            self._rtype = TYPE_LOOKUP[rdata_type]
            if rdata_type == SOA and len(args) == 2:
                args += ((SERIAL, 3600, 10800, 86400, 3600),)
            rdata = rdata_type(*args)

        if rtype:
            self._rtype = rtype
        self._rname = rname
        self.kwargs = dict(
            rdata=rdata,
            ttl=self.sensible_ttl() if ttl is None else ttl,
            **kwargs,
        )

    def try_rr(self, q):
        if q.qtype == QTYPE.ANY or q.qtype == self._rtype:
            return self.as_rr(q.qname)

    def as_rr(self, alt_rname):
        return RR(rname=self._rname or alt_rname, rtype=self._rtype, **self.kwargs)

    def sensible_ttl(self):
        if self._rtype in (QTYPE.NS, QTYPE.SOA):
            return 86400
        else:
            return 300

    @property
    def is_soa(self):
        return self._rtype == QTYPE.SOA

# ----------------- Descargar zonas -----------------

ZONES = {}

try:
    get_zones = requests.get("https://raw.githubusercontent.com/RiiConnect24/DNS-Server/master/dns_zones.json", timeout=10)
    zones = json.loads(get_zones.text)

    for zone in zones:
        if zone["type"] == "a":
            ZONES[zone["name"]] = [ Record(A, zone["value"]) ]
        elif zone["type"] == "p":
            ZONES[zone["name"]] = [ Record(A, socket.gethostbyname(zone["value"])) ]

    gui_log("[INFO] DNS information downloaded successfully.")

except Exception as e:
    messagebox.showerror("Error", "Couldn't load DNS zones:\n" + str(e))
    sys.exit(1)

# ----------------- Resolver (con fix conntest) -----------------

class Resolver:
    def __init__(self):
        self.zones = {DNSLabel(k): v for k, v in ZONES.items()}

    def resolve(self, request, handler):

        # ---- FIX conntest Nintendo ----
        qname_str = str(request.q.qname)

        if "conntest.nintendowifi.net" in qname_str:
            reply = request.reply()
            reply.add_answer(RR(qname_str, QTYPE.A, rdata=A(MY_IP), ttl=60))
            return reply
        # --------------------------------

        reply = request.reply()
        zone = self.zones.get(request.q.qname)

        if zone is not None:
            gui_log(str(request.q.qname))
            for zone_records in zone:
                rr = zone_records.try_rr(request.q)
                rr and reply.add_answer(rr)
        else:
            found = False
            gui_log(str(request.q.qname))
            for zone_label, zone_records in self.zones.items():
                if request.q.qname.matchSuffix(zone_label):
                    try:
                        soa_record = next(r for r in zone_records if r.is_soa)
                    except StopIteration:
                        continue
                    else:
                        reply.add_answer(soa_record.as_rr(zone_label))
                        found = True
                        break
            if not found:
                if "nintendowifi.net" in str(request.q.qname):
                    reply.add_answer(RR(str(request.q.qname),QTYPE.A,rdata=A("95.217.77.151"),ttl=60))
                else:
                    reply.add_answer(RR(str(request.q.qname),QTYPE.A,
                        rdata=A(socket.gethostbyname_ex(str(request.q.qname))[2][0]),ttl=60))

        return reply

resolver = Resolver()
dnsLogger = RiiConnect24DNSLogger()

servers = []
running = False

# ----------------- Mini servidor HTTP para conntest -----------------

class ConnTestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"<html><body>OK</body></html>")

    def log_message(self, format, *args):
        return

def start_conntest_server():
    try:
        server = HTTPServer((MY_IP, 80), ConnTestHandler)
        server.serve_forever()
    except Exception as e:
        gui_log("[ERROR] ConnTest HTTP server failed: " + str(e))

# ----------------- Control de servidor -----------------

def start_server():
    global servers, running
    if running:
        return

    gui_log("[INFO] Starting DNS server in 5 seconds...")
    gui_log("[INFO] Prepare your Wii / DS connection now...")

    def delayed_start():
        global servers, running
        try:
            time.sleep(5)

            servers = [
                DNSServer(resolver=resolver, port=53, address=MY_IP, tcp=True, logger=dnsLogger),
                DNSServer(resolver=resolver, port=53, address=MY_IP, tcp=False, logger=dnsLogger),
            ]

            for s in servers:
                s.start_thread()

            threading.Thread(target=start_conntest_server, daemon=True).start()

            running = True
            gui_log("[INFO] RiiConnect24 DNS Server started.")
            gui_log("[INFO] ConnTest HTTP server started (port 80).")
            gui_log("[INFO] Waiting for Wii / DS DNS requests...")

        except PermissionError:
            messagebox.showerror("Permission error", "Run this program as Administrator / root")
        except Exception as e:
            gui_log("[ERROR] Failed to start DNS server: " + str(e))

    threading.Thread(target=delayed_start, daemon=True).start()

def stop_server():
    global servers, running
    if not running:
        return

    for s in servers:
        s.stop()

    running = False
    gui_log("[INFO] DNS Server stopped.")

# ----------------- Botones -----------------

frame = tk.Frame(left_frame, bg="black")
frame.pack(pady=5)

tk.Button(frame, text="Iniciar servidor", width=20, command=start_server).pack(side="left", padx=10)
tk.Button(frame, text="Detener servidor", width=20, command=stop_server).pack(side="left", padx=10)

# ----------------- Ejecutar GUI -----------------

root.mainloop()
