import os
import json
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# 1. Define los permisos que necesitas
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

# 2. Carga tus credenciales
flow = InstalledAppFlow.from_client_secrets_file(
    './client_secret_722584203991-psbocitc7vdn81btjf8en3ujf6b78gi0.apps.googleusercontent.com.json', SCOPES)
creds = flow.run_local_server(port=0)

# 3. Crea el servicio de Drive
service = build('drive', 'v3', credentials=creds)

# 4. Configura el webhook (canal de notificaciones)
channel = {
    "id": "mi-unico-id-canal-12345",  # ID único del canal (puede ser cualquier string único)
    "type": "web_hook",
    "address": "https://f1dc-2001-1388-4a01-972a-10d8-e718-2cbf-dcb0.ngrok-free.app/webhook"  # Tu URL pública de webhook
}

# 5. Inicia la suscripción al canal
response = service.changes().watch(body=channel, pageToken=service.changes().getStartPageToken().execute()['startPageToken']).execute()

# 6. Muestra la respuesta
print("✅ Suscripción activa.")
print(json.dumps(response, indent=2))
