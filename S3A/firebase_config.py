
import os
import firebase_admin
from firebase_admin import credentials, messaging

RUTA_CREDENCIALES_TRESASES = "Applications/NotificacionesPush/archivos/s3a_json.json"

RUTA_CREDENCIALES_FRUIT_TRUCK = "Applications/NotificacionesPush/archivos/ft_58015.json"


RUTA_CREDENCIALES_TRESASES_CRON = "/home/s3a/S3A/Applications/NotificacionesPush/archivos/s3a_json.json"

def inicializar_firebase():
    if os.path.exists(RUTA_CREDENCIALES_TRESASES):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(RUTA_CREDENCIALES_TRESASES)
                firebase_admin.initialize_app(cred)
                return "inicio"
            return "ya iniciado"
        except Exception as e:
            return str(e)
        
def inicializar_firebase_Fruit_Truck():
    if os.path.exists(RUTA_CREDENCIALES_FRUIT_TRUCK):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(RUTA_CREDENCIALES_FRUIT_TRUCK)
                firebase_admin.initialize_app(cred)
                return "inicio"
            return "ya iniciado"
        except Exception as e:
            return str(e)

def inicializar_firebase_cron():
    if os.path.exists(RUTA_CREDENCIALES_TRESASES_CRON):
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(RUTA_CREDENCIALES_TRESASES_CRON)
                firebase_admin.initialize_app(cred)
                return "1"
            return "0"
        except Exception as e:
            return str(e)