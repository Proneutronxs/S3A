
from django.utils import timezone
from django.db import connections
from Applications.TresAses.models import *
from datetime import datetime




#### INSERTA CAMBIO DE CONTRASEÑA

def insertar_registro_pass(usuario, contraseña_vieja, contraseña_nueva):
    try:
        fecha_actual = timezone.now()
        nuevo_registro = CapturaContraseñas(
            Usuario=usuario,
            ContraseñaVieja=contraseña_vieja,
            ContraseñaNueva=contraseña_nueva,
            Fecha=fecha_actual
        )
        nuevo_registro.save()
        return True
    except Exception as e:
        print(e)
        return False
    
def insertar_registro_error_sql(aplicacion,funcion,usuario,error):
    try:
        fecha_actual = timezone.now()
        nuevo_registro = CapturaErroresSQL(
            Aplicacion=aplicacion,
            Funcion=funcion,
            Usuario=usuario,
            Error=error,
            Fecha=fecha_actual
        )
        nuevo_registro.save()
        return True
    except Exception as e:
        return False
    
def insertar_registros_realizados(aplicacion,funcion,usuario,accion,realiza):
    try:
        fecha_actual = timezone.now()
        nuevo_registro = CapturaRegistros(
            Aplicacion=aplicacion,
            Funcion=funcion,
            Usuario=usuario,
            Accion=accion,
            Realiza=realiza,
            Fecha=fecha_actual
        )
        nuevo_registro.save()
        return True
    except Exception as e:
        return False
    

def inyectaData(Funcion,Descripcion,Fecha,FechaInicio,FechaFinal,Dia,Sector):
    values = [Funcion,Descripcion,Fecha,FechaInicio,FechaFinal,Dia,Sector]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "INSERT INTO Data_Funciones (Funcion,Descripcion,Fecha,FechaInicio,FechaFinal,Dia,Sector) VALUES (%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sql,values)
            cursor.commit()
    except Exception as e:
        insertar_registro_error_sql("TareasHE","inyectaData","errores",str(e))
        
    finally:
        connections['TRESASES_APLICATIVO'].close()   


def obtenerFechaActual():
    fecha_actual = datetime.now()
    fecha = fecha_actual.strftime('%d/%m/%Y')
    return fecha

def obtenerFechaActualUSA():
    fecha_actual = datetime.now()
    fecha = fecha_actual.strftime('%Y-%m-%d')
    return fecha

def obtenerHoraActual():
    hora_actual = datetime.now()
    hora = hora_actual.strftime('%H:%M')
    return hora

