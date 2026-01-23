# Sooramaru's DNS DS

**Español abajo / English below**

---

## 🇬🇧 English

### Sooramaru's DNS DS

A graphical, local DNS server for Nintendo Wii / Nintendo DS revival services.

This project is a **fork of the RiiConnect24 DNS Server** (based on sudomemoDNS by Austin Burk), enhanced with a graphical interface and several quality‑of‑life improvements.

It allows your Wii / DS to connect to revival services such as **RiiConnect24**, **Wiimmfi**, and other WFC replacements using a **local DNS server running on your PC**.

---

### ✨ Features

* 🖥️ Graphical interface (Tkinter)
* 🟢 Fully local DNS server (no external DNS required)
* 🧪 ConnTest freeze fix (DNS + built‑in HTTP server)
* ⏱️ Startup delay before launching the server
* 📄 Supports local `dns_zones.json` (offline mode)
* 🔄 Reload zones without restarting
* 🌐 Update zones directly from GitHub
* 🧹 Clear log button
* 🖤 Terminal‑style UI (black background, green text)

---

### ⚙️ Requirements

* Windows (recommended)
* Python 3.8+ (only needed if running from source)
* Administrator privileges (required for ports 53 and 80)

Python dependencies:

```bash
pip install dnslib requests
```

---

### 🚀 How to Use

1. Run the program as **Administrator**.
2. Set your Wii / DS DNS settings to:

```
Primary DNS:   <IP of your PC>
Secondary DNS: 1.1.1.1
```

3. Click **“Iniciar servidor / Start server”**.
4. Wait 5 seconds for the server to start.
5. Test the connection on your Wii / DS.

If everything is correct, the connection test will pass instantly (no freeze).

---

### 🧪 Testing ConnTest

You can test the built‑in HTTP ConnTest server in your browser:

```
http://<YOUR_PC_IP>/
```

It should display:

```
OK
```

---

### 📄 DNS Zones

The server loads zones in this order:

1. Local file: `dns_zones.json`
2. If not found, it downloads from the official RiiConnect24 repository

You can:

* Edit `dns_zones.json` manually
* Reload it live using **“Reload zones”**
* Update it from GitHub using **“Update zones”**

---

### ⚠️ Disclaimer

This project is **not affiliated with Nintendo or RiiConnect24**.

It is intended for:

* Educational purposes
* Compatibility and preservation
* Private home network usage

All trademarks belong to their respective owners.

---

### ❤️ Credits

Original projects:

* sudomemoDNS – Austin Burk
* RiiConnect24 DNS Server – RiiConnect24 Team

Fork and enhancements:

* Sooramaru

---

### 📜 License

This project follows the original license of the RiiConnect24 DNS Server.
Please keep original copyright notices when redistributing.

---

## 🇪🇸 Español

### Sooramaru's DNS DS

Servidor DNS local con interfaz gráfica para servicios revival de Nintendo Wii / Nintendo DS.

Este proyecto es un **fork del RiiConnect24 DNS Server** (basado en sudomemoDNS de Austin Burk), mejorado con una interfaz gráfica y varias funciones adicionales.

Permite que tu Wii / DS se conecte a servicios revival como **RiiConnect24**, **Wiimmfi** y otros reemplazos de WFC usando un **servidor DNS local ejecutándose en tu PC**.

---

### ✨ Funciones

* 🖥️ Interfaz gráfica (Tkinter)
* 🟢 Servidor DNS completamente local
* 🧪 Fix del bug de ConnTest (DNS + servidor HTTP integrado)
* ⏱️ Retardo antes de iniciar el servidor
* 📄 Soporte para `dns_zones.json` local (modo offline)
* 🔄 Recarga de zonas sin reiniciar
* 🌐 Actualización directa desde GitHub
* 🧹 Botón para limpiar el log
* 🖤 Interfaz estilo terminal (fondo negro, texto verde)

---

### ⚙️ Requisitos

* Windows (recomendado)
* Python 3.8+ (solo si usas el código fuente)
* Ejecutar como Administrador (puertos 53 y 80)

Dependencias de Python:

```bash
pip install dnslib requests
```

---

### 🚀 Uso

1. Ejecuta el programa como **Administrador**.
2. Configura el DNS de tu Wii / DS así:

```
DNS Primario:   <IP de tu PC>
DNS Secundario: 1.1.1.1
```

3. Presiona **“Iniciar servidor”**.
4. Espera 5 segundos.
5. Prueba la conexión en tu consola.

Si todo está correcto, la prueba de conexión pasará al instante (sin congelarse).

---

### 🧪 Probar ConnTest

Puedes probar el servidor HTTP desde tu navegador:

```
http://<IP_DE_TU_PC>/
```

Debe mostrar:

```
OK
```

---

### 📄 Zonas DNS

El servidor carga las zonas en este orden:

1. Archivo local: `dns_zones.json`
2. Si no existe, las descarga desde el repositorio oficial de RiiConnect24

Puedes:

* Editar `dns_zones.json` manualmente
* Recargarlo con **“Recargar zonas”**
* Actualizarlo con **“Actualizar zonas”**

---

### ⚠️ Aviso Legal

Este proyecto **no está afiliado con Nintendo ni con RiiConnect24**.

Está hecho con fines de:

* Educación
* Compatibilidad
* Preservación digital
* Uso privado en redes domésticas

Todas las marcas pertenecen a sus respectivos dueños.

---

### ❤️ Créditos

Proyectos originales:

* sudomemoDNS – Austin Burk
* RiiConnect24 DNS Server – Equipo RiiConnect24

Fork y mejoras:

* Sooramaru

---

### 📜 Licencia

Este proyecto mantiene la licencia original del RiiConnect24 DNS Server.
Conserva los avisos de copyright al redistribuir.
