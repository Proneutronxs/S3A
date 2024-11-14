
import os
import firebase_admin
from firebase_admin import credentials, messaging

RUTA_CREDENCIALES = "Applications/NotificacionesPush/archivos/s3a_json.json"

def inicializar_firebase():
    if os.path.exists(RUTA_CREDENCIALES):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(RUTA_CREDENCIALES)
                firebase_admin.initialize_app(cred)
        except Exception as e:
            pass

