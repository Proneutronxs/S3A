
from S3A.firebase_config import firebase_admin, messaging


def enviar_notificacion_chofer_solicita(token, body, pestaña):
    if not token or not body or not pestaña:
        return 'bodys' 
    try:
        message = messaging.Message(
            data={
                "title": "Tres Ases",
                "body": body,
                "Pestaña": pestaña
            },
            token=token,
        )
        response = messaging.send(message)
        return '1' if response else '0'
    except Exception as e:
        return 'excepcion' + str(e)
