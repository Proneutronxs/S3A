
from S3A.firebase_config import firebase_admin, messaging
from S3A.firebase_config import inicializar_firebase, inicializar_firebase_Fruit_Truck
from django.db import connections


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
    

    
def enviar_notificacion_Tres_Ases(token, body, pestaña, ID_CNG):
    inicio = inicializar_firebase()
    if not token or not body or not pestaña:
        return 'Faltan parámetros requeridos' 
    try:
        message = messaging.Message(
            data={
                "Title": "Tres Ases",
                "Body": body,
                "Pestaña": pestaña,
                "ID_CNG": ID_CNG # Usar el ID_CNG pasado como parámetro
            },
            token=token,
        )
        response = messaging.send(message)
        return '1' if response else '0'
    except Exception as e:
        return 'Excepción en envío de notificación: ' + str(e)
    

def debug_error(usuario, body, error):
    try:
        with connections['BD_DEBUG'].cursor() as cursor:
            sql = """ 
                    INSERT INTO TB_DEBUG (USUARIO, FECHA, BODY)
                    VALUES (%s, NOW(), %s)
                """
            if error:
                body += f" - Error: {error}"
            cursor.execute(sql, (usuario, body))
            connections['BD_DEBUG'].commit()
    except Exception as e:
        pass



    
def enviar_notificacion_Tres_Ases_Cron(token, body, pestaña, ID_CNG):
    if not token or not body or not pestaña:
        debug_error("FIREBASE-NT", ID_CNG, "FALTAN PARAMETROS")
        return 'Faltan parámetros requeridos' 
    try:
        message = messaging.Message(
            data={
                "Title": "Tres Ases",
                "Body": body,
                "Pestaña": pestaña,
                "ID_CNG": ID_CNG # Usar el ID_CNG pasado como parámetro
            },
            token=token,
        )
        response = messaging.send(message)
        debug_error("FIREBASE-NT", ID_CNG, "-" + str(response))
        return '1' if response else '0'
    except Exception as e:
        debug_error("FIREBASE-NT", ID_CNG, str(e))
        return 'Excepción en envío de notificación: ' + str(e)