
from S3A.firebase_config import firebase_admin, messaging
from S3A.firebase_config import inicializar_firebase, inicializar_firebase_Fruit_Truck


def enviar_notificacion_chofer_solicita(token, body, pestaña):
    inicio = inicializar_firebase()
    if not token or not body or not pestaña:
        return 'bodys' 
    try:
        message = messaging.Message(
            data={
                "Title": "Tres Ases",
                "Body": body,
                "Pestaña": pestaña,
                "ID_CNG": "0"
            },
            token=token,
        )
        response = messaging.send(message)
        return '1' if response else '0'
    except Exception as e:
        return 'excepcion ' + str(inicio)


def notificaciones_Fruit_Truck(Token, Body, Tipo, Habilitado, ID_CVN, Destinos):
    inicializar_firebase_Fruit_Truck()
    if not Token or not Body or not Destinos:
        return 'bodys' 
    try:
        message = messaging.Message(
            data={
                "Title": "Fruit Truck",
                "Body": Body,
                "Tipo": Tipo,   ## N ACTUALISA LA TABLA DE NUEVSO DESTINOS - V ACTUALIZA LA DEL VIAJE ASIGNADO TABLAS QUE RECIBE LA NOTIFICACION
                "Habilitado": Habilitado,
                "ID_CVN": ID_CVN,
                "Destinos": Destinos ## S ES PARA ACTUALIZAR LOS DESTINOS  N NO ACTUALIZA LOS DESTINOS
            },
            token=Token,
        )
        response = messaging.send(message)
        return '1' if response else '0'
    except Exception as e:
        return 'excepcion ' 
    
def enviar_notificacion_Tres_Ases(token, body, pestaña,ID_CNG):
    inicio = inicializar_firebase()
    if not token or not body or not pestaña:
        return 'bodys' 
    try:
        message = messaging.Message(
            data={
                "Title": "Tres Ases",
                "Body": body,
                "Pestaña": pestaña,
                "ID_CNG": ID_CNG
            },
            token=token,
        )
        response = messaging.send(message)
        return '1' if response else '0'
    except Exception as e:
        return 'excepcion ' + str(inicio)