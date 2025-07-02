from flask import Flask, request
import pickle
import os
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def load_credentials():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception("No se encontraron credenciales válidas. Ejecuta authorize.py primero.")
    return creds

@app.route('/webhook', methods=['POST'])
def webhook():
    print(" ¡Cambio detectado en Google Drive!")
    print("Encabezados:", dict(request.headers))
    
    resource_uri = request.headers.get('X-Goog-Resource-Uri')
    page_token = None
    if resource_uri:
        query = urlparse(resource_uri).query
        params = parse_qs(query)
        page_token = params.get('pageToken', [None])[0]
    
    if not page_token:
        print(" No se encontró pageToken en la notificación.")
        return '', 200
    
    try:
        creds = load_credentials()
        service = build('drive', 'v3', credentials=creds)
        
        response = service.changes().list(pageToken=page_token, spaces='drive').execute()
        
        for change in response.get('changes', []):
            file = change.get('file')
            if file:
                print(f" Archivo cambiado: {file.get('name')} (ID: {file.get('id')})")
            else:
                print("️ Cambio sin archivo asociado:", change)
        
        if 'newStartPageToken' in response:
            print(" Nuevo startPageToken:", response['newStartPageToken'])
        
    except Exception as e:
        print(" Error al consultar cambios:", e)
    
    return '', 200

if __name__ == '__main__':
    app.run(port=5000)
