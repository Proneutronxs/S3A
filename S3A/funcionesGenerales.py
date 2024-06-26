
from django.utils import timezone
from django.db import connections
from Applications.TresAses.models import *
from datetime import datetime, timedelta
import calendar




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

def registroRealizado(Usuario,Descripcion,Body):
    values = [Usuario,Descripcion,Body]
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = "INSERT INTO RegistroRealiza (Usuario,Descripcion,FechaAlta,Body) VALUES (%s,%s,GETDATE(),%s)"
            cursor.execute(sql,values)
            cursor.commit()
    except Exception as e:
        insertar_registro_error_sql("FUNCION REGISTRO","registroRealizado","errores",str(e))

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

def buscaCentroCostosPorUsuario(codigo,usuario):
    data = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """
                    DECLARE @P_Codigo VARCHAR(255);
                    DECLARE @P_Usuario VARCHAR(255);
                    SET @P_Codigo = %s;
                    SET @P_Usuario = %s;
                    IF EXISTS (SELECT 1 FROM Parametros_Aplicativo WHERE Usuario = @P_Usuario AND Codigo = @P_Codigo)
                    BEGIN
                        SELECT Texto
                        FROM Parametros_Aplicativo
                        WHERE Codigo = @P_Codigo AND Usuario = @P_Usuario;
                    END
                    ELSE
                    BEGIN
                        SELECT Texto
                        FROM Parametros_Aplicativo
                        WHERE Codigo = @P_Codigo AND Usuario IS NULL;
                    END
                """
            cursor.execute(sql, [codigo,usuario])
            consulta = cursor.fetchone()
            if consulta:
                data = str(consulta[0]).split('-')
                return data
            else:
                return data
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("CODIGO USUARIO","BUSCA DATA TEXTO",usuario,error)
        return data


from datetime import datetime

def fecha_hora_actual_texto():
    dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']

    meses = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']
  
    ahora = datetime.now()
    
    dia_semana = dias_semana[ahora.weekday()]
    dia_mes = ahora.day
    mes = meses[ahora.month - 1]
    año = ahora.year
    
    hora = ahora.hour
    minutos = ahora.minute
    
    fecha_hora_str = f"{dia_semana} {dia_mes} de {mes} del {año} - {hora}:{minutos:02d} Hs."
    
    return fecha_hora_str

def NombreCentro(cc):
    try:
        with connections['ISISPayroll'].cursor() as cursor:
            sql = "SELECT DescrCtroCosto " \
                "FROM CentrosCostos " \
                "WHERE Regis_CCo = %s"
            cursor.execute(sql,[cc])
            consulta = cursor.fetchone()
            if consulta:
                ids = str(consulta[0])
                return ids
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("GENERALES","NOMBRE CENTRO","usuario",error)
        return ""

def NombreEspecie(id):
    try:
        with connections['S3A'].cursor() as cursor:
            sql = "SELECT RTRIM(Nombre) " \
                "FROM Especie " \
                "WHERE IdEspecie = %s"
            cursor.execute(sql,[id])
            consulta = cursor.fetchone()
            if consulta:
                ids = str(consulta[0])
                return ids
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("GENERALES","NOMBRE ESPECIE","usuario",error)
        return ""
    
def obtener_dias_mes(año, mes):
    año = int(año)
    mes = int(mes) 
    num_dias_mes = calendar.monthrange(año, mes)[1]
    primer_dia_semana = calendar.monthrange(año, mes)[0]
    
    dias_mes = [f"{año}-{mes:02d}-{dia:02d}" for dia in range(1, num_dias_mes + 1)]
    
    return dias_mes

def formatear_fecha_a_dia_mes(fecha):
    año, mes, dia = fecha.split('-')
    fecha_formateada = f"{dia}/{mes}"
    
    return fecha_formateada

def obtener_año_actual():
    import datetime
    año_actual = datetime.datetime.now().year
    return str(año_actual)

def obtener_fechas_entre(fecha_inicio, fecha_fin):
    fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
    
    dias_entre_fechas = []
    while fecha_inicio <= fecha_fin:
        dias_entre_fechas.append(fecha_inicio.strftime('%Y-%m-%d'))
        fecha_inicio += timedelta(days=1)
    
    return dias_entre_fechas


def formatear_fecha(fecha):
    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d')
        fecha_formateada = fecha_obj.strftime('%d/%m/%Y')
        return fecha_formateada
    except ValueError:
        return "Formato de fecha incorrecto"