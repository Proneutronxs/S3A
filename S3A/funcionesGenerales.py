
from django.utils import timezone
from django.db import connections
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.http import HttpResponse, Http404
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
    
# def insertar_registro_error_sql(aplicacion,funcion,usuario,error): #`Aplicacion`, `Funcion`, `Usuario`, `Error`, `Fecha`
#     try:
#         fecha_actual = timezone.now()
#         nuevo_registro = CapturaErroresSQL(
#             Aplicacion=aplicacion,
#             Funcion=funcion,
#             Usuario=usuario,
#             Error=error,
#             Fecha=fecha_actual
#         )
#         nuevo_registro.save()
#         return True
#     except Exception as e:
#         return False
    
def insertar_registro_error_sql(aplicacion,funcion,usuario,error):
    values = [aplicacion,funcion,usuario,error]
    try:
        with connections['default'].cursor() as cursor:
            sql = "INSERT INTO TresAses_capturaerroressql (Aplicacion,Funcion,Usuario,Error,Fecha) VALUES (%s,%s,%s,%s,NOW())"
            cursor.execute(sql,values)
            cursor.commit()
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

def obtenerHorasArchivo():
    fecha_actual = datetime.now()
    hora = fecha_actual.strftime('%H_%M_%S')
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
    
def formatear_moneda(numero):
    numero = float(numero)
    return "${:,.2f}".format(numero).replace(",", "#").replace(".", ",").replace("#", ".")

def obtener_calibres(calibres):
    calibre_map = {
    "AAAA": 90,
    "AAA": 80,
    "AA": 70,
    "A": 60,
    "B": 50,
    "C": 40
    }
    calibres_lista = [x.strip() for x in calibres.split("-")]
    if calibres_lista[0].isalpha():
        calibres_lista = [calibre_map.get(calibre, 0) for calibre in calibres_lista]
    else:
        calibres_lista = [int(calibre) for calibre in calibres_lista]
    return calibres_lista

def decode_crc_(crc, p_calibre, p_segundo):
    if crc == 0:
        return 0
    else:
        return round((crc * 100 * p_calibre) / (3.1415 * (p_segundo+1)))
    
def formato_moneda(tipo,valor):
    if isinstance(valor, str):
        valor = valor.replace(",", ".")
    return tipo + f" {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


### GET LISTA CENTROS
def listaCentros(request):
    if request.method == 'GET':
        try:
            with connections['ISISPayroll'].cursor() as cursor:
                sql = """
                        SELECT Regis_Cco AS ID, CONVERT(VARCHAR(27),(AbrevCtroCosto + ' - ' + DescrCtroCosto)) AS CENTRO
                        FROM CentrosCostos
                        ORDER BY CENTRO
                    """
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = [{'Codigo': '0', 'Descripcion': 'TODOS'}]
                    for row in consulta:
                        codigo = str(row[0])
                        descripcion = str(row[1])
                        datos = {'Codigo': codigo, 'Descripcion': descripcion}
                        lista_data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FUNCIONES GENERAL","LISTA CENTROS","usuario",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['ISISPayroll'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
def listaAbrevCentros(request):
    if request.method == 'GET':
        try:
            with connections['ISISPayroll'].cursor() as cursor:
                sql = """
                        SELECT Regis_Cco AS ID, RTRIM(AbrevCtroCosto) AS CENTRO
                        FROM CentrosCostos
                        ORDER BY CENTRO
                    """
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = [{'Codigo': '0', 'Descripcion': 'TODOS'}]
                    listado_descripcion = [{'Codigo': '0', 'Descripcion': 'TODO'}, {'Codigo': 'PT', 'Descripcion': 'POR TANTO'},{'Codigo': 'pd', 'Descripcion': 'POR DÍA'}, {'Codigo': 'FE', 'Descripcion': 'FERIADO'},{'Codigo': 'SD', 'Descripcion': 'SAB/DOM'},{'Codigo': 'AR', 'Descripcion': 'ARREGLOS'}]
                    listado_pagos = [{'Codigo': '0', 'Descripcion': 'TODO'}, {'Codigo': 'A', 'Descripcion': 'ADICIONAL'},{'Codigo': 'R', 'Descripcion': 'RECIBO'}]
                    for row in consulta:
                        codigo = str(row[0])
                        descripcion = str(row[1])
                        datos = {'Codigo': codigo, 'Descripcion': descripcion}
                        lista_data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data, 'Descripcion': listado_descripcion, 'Pagos':listado_pagos})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FUNCIONES GENERAL","LISTA CENTROS","usuario",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['ISISPayroll'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
    
@csrf_exempt
def listaPersonalPorCentro(request): ###listado de personal por listado de centros
    if request.method == 'POST':
        centros = request.POST.get('Centro')
        listaCentros = centros.split(',')
        centros_str = ','.join(listaCentros)
        centro = "0" if listaCentros == ['0'] else "1"
        try:
            with connections['ISISPayroll'].cursor() as cursor:
                sql = f"""
                        DECLARE @@Centro INT;
                        SET @@Centro = %s
                        SELECT CodEmpleado AS LEGAJO, CONVERT(VARCHAR(31), (CONVERT(VARCHAR(15), CodEmpleado) + ' - ' + ApellidoEmple + ' ' + NombresEmple)) AS NOMBRE 
                        FROM Empleados
                        WHERE BajaDefinitivaEmple = '2' AND (@@Centro = '0' OR Regis_CCo IN ({centros_str}))
                        ORDER BY ApellidoEmple
                    """
                cursor.execute(sql, [centro])
                consulta = cursor.fetchall()

                if consulta:
                    lista_data = [{'Legajo': '0', 'Nombre': 'TODOS'}]
                    for row in consulta:
                        codigo = str(row[0])
                        descripcion = str(row[1])
                        datos = {'Legajo': codigo, 'Nombre': descripcion}
                        lista_data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("FUNCIONES GENERAL","LISTA PERSONAL POR CENTRO","usuario",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['ISISPayroll'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})















####### NUEVAS FUNCIONES PARTE NUEVA FUNCIONES DE MODULOS MD



def Centros_Modulos_Usuarios(codigo,usuario):
    values = [codigo,usuario]
    lista_data = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """
                    EXEC GENERAL_CENTROS_POR_USUARIO %s, %s
                """
            cursor.execute(sql, values)
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    lista_data.append({
                        "IdCentro": str(row[0]),
                        "Descripcion": str(row[1])
                    })
                return lista_data
            else:
                return lista_data
    except Exception as e:
        return lista_data

