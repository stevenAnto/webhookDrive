# 📡 Webhook para Google Drive con Flask

Este proyecto configura un **webhook** en Python usando **Flask** para detectar cambios en tu cuenta de **Google Drive** mediante la API v3.

## 📁 Estructura del Proyecto

```bash
.
├── ambiente/                         # Entorno virtual (Crear su entorno virtual)
├── authorize.py                     # Script para autenticar y generar token
├── client_secret_XXXX.json          # Credenciales OAuth2 (agregarlo)
├── token.pickle                     # Token de acceso generado por authorize.py
├── watch_drive.py                   # Habilita el webhook en Google Drive(Crea el canal de escucha ejecutarlo una vez)
└── webhook_drive.py                 # Servidor Flask que recibe notificaciones
```

## 🧰 Requisitos

- Python 3.12.3
- Cuenta de Google
- Proyecto habilitado en [Google Cloud Console](https://console.cloud.google.com/)
- Ngrok (para exponer tu servidor Flask en internet)

## 🔐 Configuración de Google Cloud

1. Habilita la API de Google Drive en tu proyecto.
2. Crea una credencial OAuth 2.0 (tipo aplicación de escritorio).
3. Descarga el archivo `client_secret_XXXX.json` y colócalo en la raíz del proyecto.

## 🚀 Cómo Ejecutar

### 1. Crear entorno virtual

```bash
python3.12 -m venv ambiente
source ambiente/bin/activate
pip install -r requirements.txt
```


### 2. Autenticarse con Google

```bash
python authorize.py
```

Esto abrirá un navegador para que autorices tu cuenta y guardará el token en `token.pickle`.

### 3. Iniciar el servidor Flask

```bash
python webhook_drive.py
```

### 4. Exponer el puerto con Ngrok

En otra terminal:

```bash
ngrok http 5000
```

Copia la URL HTTPS que te da Ngrok.

### 5. Activar el webhook

 `watch_drive.py` si es necesario y luego ejecútalo:

```bash
python watch_drive.py
```

Este script notificará a Google Drive para empezar a enviar cambios a tu endpoint expuesto por Ngrok.

## 🧪 Prueba de Cambios

Cada vez que subas, edites o elimines un archivo en tu Drive, recibirás una notificación y se imprimirá información en consola.

## 🛡️ .gitignore sugerido



# Archivos sensibles
client_secret_*.json
token.pickle
```

## 📝 Créditos

Desarrollado como ejemplo de integración entre Flask y Google Drive Webhooks.

---
