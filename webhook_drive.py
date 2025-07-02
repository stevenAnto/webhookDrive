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
    print("***********************\n")
    
    resource_uri = request.headers.get('X-Goog-Resource-Uri')
    page_token = None
    token_path= 'last_token.txt'
    if resource_uri:
        print("There is resouci+iru")
        query = urlparse(resource_uri).query
        params = parse_qs(query)
        page_token = params.get('pageToken', [None])[0]
    

    if os.path.exists(token_path):
        print("encontramos el nuevo token para el cambio")
        with open(token_path, 'r') as f:
            page_token = f.read().strip()
        print("page_token",page_token)
    
    if not page_token:
        print(" No se encontró pageToken en la notificación.")
        return '', 200
    
    try:
        creds = load_credentials()
        service = build('drive', 'v3', credentials=creds)
        
        response = service.changes().list(pageToken=page_token, spaces='drive').execute()
        
        for change in response.get('changes', []):
            file = change.get('file')
            removed = change.get('removed', False)
            change_type = change.get('changeType', 'unknown')
            file_id = None
            file_name = None

            if removed:
                # Archivo eliminado
                file_id = change.get('fileId', 'Desconocido')
                print(f" Archivo eliminado: ID={file_id}")
            elif file:
                # Archivo creado o modificado
                file_id = file.get('id')
                file_name = file.get('name')
                print(f" Archivo cambiado: {file_name} (ID: {file_id})")
                
                # Ahora podemos obtener detalles adicionales del archivo
                try:
                   file_detail = service.files().get(fileId=file_id, fields="id, name, mimeType, modifiedTime, owners, trashed").execute()
                   print(" Detalles del archivo:")
                   print(f"  Tipo MIME: {file_detail.get('mimeType')}")
                   print(f"  Modificado: {file_detail.get('modifiedTime')}")
                   print(f"  Propietarios: {[owner.get('emailAddress') for owner in file_detail.get('owners', [])]}")
                   print(f"  Papelera: {file_detail.get('trashed')}")
                except Exception as e:
                   print(f"  No se pudo obtener detalles: {e}")
            else:
                print(" Cambio sin archivo asociado:", change)
            print("------------\n")
        
        if 'newStartPageToken' in response:
            new_token = response['newStartPageToken']
            with open(token_path, 'w') as f:
                f.write(new_token)
            print(" Nuevo startPageToken:", response['newStartPageToken'])
        
    except Exception as e:
        print(" Error al consultar cambios:", e)
    
    return '', 200

if __name__ == '__main__':
    app.run(port=5000)
