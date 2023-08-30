from django.db import connections
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib



def insertaRegistro(legajo,fecha,tipo,estado):
    try:  
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "INSERT INTO Auditoria_Aplicacion_Android (Usuario, FechaHora, TipoRegistro, Estado) VALUES (%s, %s, %s, %s)"
            values = (legajo, fecha, tipo, estado)
            cursor.execute(sql, values)
            cursor.close()
    except Exception as e:
        error = str(e)
        return error
    finally:
        connections['TRESASES_APLICATIVO'].close()


#contrseña = 8vzU&Uz3iorn

def enviarCorreo(asunto, contenido, destinatario):
    remitente = 'aplicativo@tresases.com.ar'
    asunto = 'No Responder - ' + asunto
    cuerpo = contenido

    correo = MIMEMultipart()
    correo['From'] = remitente
    correo['To'] = destinatario
    correo['Subject'] = asunto

    correo.attach(MIMEText(cuerpo, 'plain'))
    servidor_smtp = smtplib.SMTP('mail.tresases.com.ar', 587)
    servidor_smtp.starttls()
    servidor_smtp.login(remitente, '1234')
    servidor_smtp.send_message(correo)
    servidor_smtp.quit()
























