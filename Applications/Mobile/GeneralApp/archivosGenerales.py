from django.db import connections




def insertaRegistro(legajo,fecha,tipo,estado):
    try:  
        with connections['default'].cursor() as cursor:
            sql = "INSERT INTO Auditoria_Aplicacion_Android (Usuario, FechaHora, TipoRegistro, Estado) VALUES (%s, %s, %s, %s)"
            values = (legajo, fecha, tipo, estado)
            cursor.execute(sql, values)
            cursor.close()
    except Exception as e:
        error = str(e)
        return error
    finally:
        connections['default'].close()