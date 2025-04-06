from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from S3A.funcionesGenerales import *
from S3A.conexionessql import *
from datetime import datetime, timedelta
import json
from Applications.Mobile.GeneralApp.archivosGenerales import insertaRegistro
from Applications.TareasProgramadas.tasks import buscaSector
from django.db import connections
from django.http import JsonResponse

# Create your views here.

### METODO PARA MOSTRAR LOS MOTIVOS (GET)
@csrf_exempt
def motrar_MotivosHE(request):
    if request.method == 'GET':
        try:
            with connections['S3A'].cursor() as cursor:
                sql = "SELECT IdMotivo AS ID, RTRIM(Descripcion) AS Motivo " \
                        "FROM RH_HE_MOTIVO " \
                        "ORDER BY Descripcion"
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    response_data = []
                    for row in consulta:
                        IdMotivo, Motivo = map(str, row)
                        data = {
                            'IdMotivo': IdMotivo,
                            'Motivo': Motivo
                        }
                        response_data.append(data)
                    datos = {'Message': 'Success', 'Data': response_data}
                    return JsonResponse(datos, safe=False)
                else:
                    response_data = {
                        'Message': 'Not Found',
                        'Nota': 'No se encontraron Motivos Cargados.' 
                    }
                    return JsonResponse(response_data)
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("HorasExtras","motrar_MotivosHE","usuario",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def obtener_fecha_hora_actual_con_milisegundos():
    import datetime 
    now = datetime.datetime.now()
    fecha_hora_actual = now.strftime("%Y-%m-%dT%H:%M:%S")
    hora = str(fecha_hora_actual) + ".000"
    return hora

###  METODO POST PARA PODER INSERTAR LAS HORAS EXTRAS PRE AUTORIZADAS EN EL SQL (BODY)
@csrf_exempt
def insert_HoraExtra(request):
    if request.method == 'POST':
        try:
            lista_tieneHE_asignada = []
            lista_hora_es_antes = []
            body = request.body.decode('utf-8')
            usuario = str(json.loads(body)['usuario'])
            fechaHora = str(json.loads(body)['actual'])
            registro = str(json.loads(body)['registro'])
            datos = json.loads(body)['Data']
            for item in datos:
                fechaAlta = obtener_fecha_hora_actual_con_milisegundos()
                Legajo = str(item['Legajo']) ### LEGAJO
                Regis_Epl = str(item['Regis_Epl'])### ID LEGAJO
                Desde = str(item['DateTimeDesde']) ### DATETIME DESDE
                Hasta = str(item['DateTimeHasta']) ### DATETIME HASTA
                idMotivo = str(item['Motivo']) ### MOTIVO
                Descripcion = str(item['Descripcion']) ### DESCRIPCION DE LA TAREA
                Arreglo = str(item['Arreglo']) ### SI SE HIZO UN ARREGLO CON RESPECTO A LA HORA
                try:
                    Importe = str(item['importeArreglo'])
                except KeyError:
                    Importe = "0"
                Sector = buscaSector(Legajo) ### TRAE EL SECTOR DE LEGAJO
                Usuario = str(item['Usuario']) ### USUARIO DE LA APLICACIÓN
                Autorizado = str(item['Autorizado']) ### RELACIONAR EL LEGAJO O BIEN CARGAR EL ID DEL AUTORIZADO
                Estado = "1" ### ESTADO PRE CARGA SIEMPRE EN 1 

                fechaHasta = retornaYYYYMMDD(Hasta)
                if es_posterior_a_actual(Hasta):
                    if buscaHoras(fechaHasta,Legajo,Desde.replace('T', ' '),Hasta.replace('T', ' ')):
                        lista_tieneHE_asignada.append(Legajo)
                    else:
                        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                            sql = "INSERT INTO HorasExtras_Sin_Procesar (Legajo, Regis_Epl, DateTimeDesde, DateTimeHasta, IdMotivo, DescripcionMotivo, Arreglo, ImpArreglo, Sector, UsuarioEncargado, Autorizado, FechaAlta, Estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                            values = (Legajo, Regis_Epl, Desde, Hasta, idMotivo, Descripcion, Arreglo, Importe, Sector, Usuario, Autorizado, fechaAlta, Estado)
                            cursor.execute(sql, values)
                else:
                    lista_hora_es_antes.append(Legajo)

            if len(lista_hora_es_antes) == 0:
                if len(lista_tieneHE_asignada) == 0:
                    nota = "Los Horas Extras se envíaron correctamente."
                    est = "E"
                    insertaRegistro(usuario,fechaHora,registro,est)
                    return JsonResponse({'Message': 'Success', 'Nota': nota})
                else:
                    nombres = []
                    for legajo in lista_tieneHE_asignada:
                        Apellido = traeApellidos(str(legajo))
                        nombres.append(Apellido)
                    nota = "Los siguientes Apellidos ya tienen asignadas horas extras en ese rango horario: \n" + ', \n'.join(nombres) + '.\nVea los horarios guardados.'
                    est = "E"
                    insertaRegistro(usuario,fechaHora,registro,est) 
                    return JsonResponse({'Message': 'Success', 'Nota': nota})
            else:
                nombres = []
                for legajo in lista_hora_es_antes:
                    Apellido = traeApellidos(str(legajo))
                    nombres.append(Apellido)
                nota = "Los siguientes Apellidos no se pueden guardar: \n" + ', \n'.join(nombres) + '.\nSólo se pueden cargar horas extras que no superen las 24hs. hacia atrás de la FECHA y HORA ACTUAL.'
                est = "E"
                insertaRegistro(usuario,fechaHora,registro,est) 
                return JsonResponse({'Message': 'Success', 'Nota': nota})
            
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("HorasExtras","insert_horaExtra","usuario",error)
            est = "F"
            insertaRegistro(usuario,fechaHora,registro,est) 
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
def es_posterior_a_actual(datetime_str):
    datetime_str = str(datetime_str).replace('T',' ')
    fecha_hora = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
    fecha_hora_actual = datetime.now()
    fecha_hora_margen = fecha_hora_actual - timedelta(days=1)
    return fecha_hora > fecha_hora_margen

### RETORNA HH:MM DE UN DATE TIME
def retornaHHMM(hora1,hora2):
    formato_entrada = "%Y-%m-%dT%H:%M:%S.%f"
    formato_salida = "%H:%M"
    horaUno = datetime.strptime(hora1, formato_entrada)
    horaDos = datetime.strptime(hora2, formato_entrada)
    horaDesde = horaUno.strftime(formato_salida)
    horaHasta = horaDos.strftime(formato_salida)
    return horaDesde, horaHasta

### RETORNA YYYY-MM-DD DE UN DATE TIME
def retornaYYYYMMDD(f2):
    formato_entrada = "%Y-%m-%dT%H:%M:%S.%f"
    formato_salida = "%Y-%m-%d"
    #fechaUno = datetime.strptime(f1, formato_entrada)
    fechaDos = datetime.strptime(f2, formato_entrada)
    #fechaDesde = fechaUno.strftime(formato_salida)
    fechaHasta = fechaDos.strftime(formato_salida)
    return fechaHasta

def verificar_rango(fecha_inicio_str, fecha_fin_str, fecha_a_verificar_str):
    fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d %H:%M:%S.%f")
    fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d %H:%M:%S.%f")
    fecha_a_verificar = datetime.strptime(fecha_a_verificar_str, "%Y-%m-%d %H:%M:%S.%f")
    return fecha_inicio <= fecha_a_verificar <= fecha_fin

def buscaHoras(fecha,legajo,dateTime1,dateTime2):
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """SELECT CONVERT(VARCHAR(23), DateTimeDesde, 25), CONVERT(VARCHAR(23), DateTimeHasta, 25) 
                FROM HorasExtras_Sin_Procesar 
                WHERE Legajo = %s AND (TRY_CONVERT(DATE, DateTimeHasta) >= %s) AND Estado <> 8 """
            cursor.execute(sql, [legajo, fecha])
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    # print(row, dateTime1)
                    # print(row, dateTime2)
                    df1 = str(row[0])
                    df2 = str(row[1])
                    if verificar_rango(df1,df2,dateTime1) or verificar_rango(df1,df2,dateTime2):
                        return True
            else:
                return False
        return False
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("HorasExtras","buscaHoras","usuario",error)
        return error

def convertir_formato_fecha_hora(fecha_hora_str):
    fecha_hora_obj = datetime.strptime(fecha_hora_str, "%Y-%m-%dT%H:%M:%S.%f")
    fecha_formateada = fecha_hora_obj.strftime("%d/%m/%Y")
    hora_formateada = fecha_hora_obj.strftime("%H:%M")

    return fecha_formateada, hora_formateada

def hora_dentro_del_rango(hora, inicio, fin):
    hora = datetime.strptime(hora, "%H:%M")
    inicio = datetime.strptime(inicio, "%H:%M")
    fin = datetime.strptime(fin, "%H:%M")

    return inicio <= hora <= fin

### TRAE EL APELLIDO DE LA HORA QUE EXISTE
def traeApellidos(legajo):
    try:
        with connections['ISISPayroll'].cursor() as cursor:
            sql = "SELECT  CONVERT(VARCHAR(25), (ApellidoEmple + ' ' + NombresEmple)) "\
                    "FROM Empleados " \
                    "WHERE CodEmpleado = %s"
            cursor.execute(sql, [legajo])
            consulta = cursor.fetchone()
            if consulta:
                apellido = str(consulta[0])
            return apellido
    except Exception as e:
        error = str(e)
        insertar_registro_error_sql("HorasExtras","traeApellidos","usuario",error)
        return error

### VERIFICA SI LA HORA INGRESADA YA TIENE ASIGNADO UNA HORA EXTRA
def verificar_solapamiento(hora_a_desde, hora_a_hasta, hora_b_desde, hora_b_hasta):
    formato = "%H:%M"

    hora_a_desde = datetime.datetime.strptime(hora_a_desde, formato).time()
    hora_a_hasta = datetime.datetime.strptime(hora_a_hasta, formato).time()
    hora_b_desde = datetime.datetime.strptime(hora_b_desde, formato).time()
    hora_b_hasta = datetime.datetime.strptime(hora_b_hasta, formato).time()

    if hora_a_desde >= hora_b_desde and hora_a_desde <= hora_b_hasta:
        return True
    if hora_a_hasta >= hora_b_desde and hora_a_hasta <= hora_b_hasta:
        return True
    if hora_b_desde >= hora_a_desde and hora_b_desde <= hora_a_hasta:
        return True
    if hora_b_hasta >= hora_a_desde and hora_b_hasta <= hora_a_hasta:
        return True

    return False

### FUNCIÓN QUE CALCULA LA CANTIDAD DE HORAS EXTRAS CON DOS VALORES DATE TIME
def calcular_CantHoras(hora1, hora2):
    #formato = "%Y-%m-%d %H:%M:%S.%f"
    formato = "%Y-%m-%d %H:%M:%S"
    dt_hora1 = datetime.strptime(hora1, formato)
    dt_hora2 = datetime.strptime(hora2, formato)
    diferencia_segundos = (dt_hora2 - dt_hora1).total_seconds()
    CantidadHoras = round(diferencia_segundos / 3600, 2)
    return CantidadHoras

### DEVUELVE LAS HORAS EXTRAS CARGADAS HASTA LA FECHA SIN QUE SE HAYAN TRANSFERIDO CON ESTADO ACTIVO = 1
@csrf_exempt
def mostrarHoraExtrasActivas(request):
    if request.method == 'GET':
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = "SELECT        PRE_CARGA_HE.CodEmpleado AS LEGAJO, PRE_CARGA_HE.ApellidoNombre AS NOMBRESyAPELLIDO, CONVERT(VARCHAR(10), PRE_CARGA_HE.Desde, 103) AS D_FECHA, CONVERT(VARCHAR(5), PRE_CARGA_HE.Desde, " \
                                                "108) AS D_HORA, CONVERT(VARCHAR(10), PRE_CARGA_HE.Hasta, 103) AS FECHA, CONVERT(VARCHAR(5), PRE_CARGA_HE.Hasta, 108) AS H_HORA, RTRIM(S3A.dbo.RH_HE_Motivo.Descripcion) AS MOTIVO, " \
                                                "PRE_CARGA_HE.idHExtra AS ID, CONVERT(VARCHAR(19), Desde, 127) AS DateTimeDesde, CONVERT(VARCHAR(19), Hasta, 127) AS DateTimeHasta " \
                        "FROM            S3A.dbo.RH_HE_Motivo INNER JOIN " \
                                                "PRE_CARGA_HE ON S3A.dbo.RH_HE_Motivo.IdMotivo = PRE_CARGA_HE.idMotivo " \
                        "WHERE        (PRE_CARGA_HE.EstadoPreCarga = '1')"
                cursor.execute(sql)
                consulta = cursor.fetchall()
                if consulta:
                    response_data = []
                    for row in consulta:
                        Legajo, ApellidoNombre, D_Fecha, D_Hora, H_Fecha, H_Hora, Motivo, Id, DateTimeInicio, DateTimeFinal = map(str, row)
                        HoraInicio = DateTimeInicio.replace('T', ' ')
                        HoraFinal = DateTimeFinal.replace('T', ' ')
                        CantHoras = str(calcular_CantHoras(HoraInicio, HoraFinal))
                        data = {
                            'Legajo': str(Legajo),
                            'ApellidoNombre': ApellidoNombre,
                            'D_Fecha': D_Fecha,
                            'D_Hora': D_Hora,
                            'H_Fecha': H_Fecha,
                            'H_Hora': H_Hora,
                            'Motivo': Motivo,
                            'IdHE': str(Id),
                            'CantHoras': CantHoras
                        }
                        response_data.append(data)
                    datos = {'Message': 'Success', 'Data': response_data}
                    return JsonResponse(datos, safe=False)
                else:
                    response_data = {
                        'Message': 'Not Found',
                        'Nota': 'No existen solicitudes de Horas Extras activas.' 
                    }
                    return JsonResponse(response_data)
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("HorasExtras","mostrarHorasExtrasActivas","usuario",error)
            response_data = {
                'Message': 'Error',
                'Nota': error
            }
            return JsonResponse(response_data)
    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)

### INSERTA LAS HORAS SELECCIONADAS EN LA TABLA PRINCIPAL DE S3A PARA SE VISTAS POR PERSONAL RRHH2
@csrf_exempt
def enviarHorasExtras(request):
    if request.method == 'POST':
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = ""
                cursor.execute(sql)
                consulta = cursor.fetchone()
                if consulta:
                    Legajo, ApellidoNombre, Desde, Hasta, Motivo, DateTimeInicio, DateTimeFinal = map(str, consulta)
                    CantHoras = str(calcular_CantHoras(DateTimeInicio, DateTimeFinal))
                    response_data = {
                        'Message': 'Success',
                        'Legajo': Legajo,
                        'ApellidoNombre': ApellidoNombre,
                        'Desde': Desde,
                        'Hasta': Hasta,
                        'Motivo': Motivo,
                        'CantHoras': CantHoras
                    }
                    return JsonResponse(response_data)
                else:
                    response_data = {
                        'Message': 'Not Found',
                        'Nota': 'No existen solicitudes de Horas Extras activas.' 
                    }
                    return JsonResponse(response_data)
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("HorasExtras","enviarHorasExtrasActivas","usuario",error)
            response_data = {
                'Message': 'Error',
                'Nota': error
            }
            return JsonResponse(response_data)
    else:
        response_data = {
            'Message': 'No se pudo resolver la petición.'
        }
        return JsonResponse(response_data)
    
def obtenerAñoActual():
    import datetime 
    now = datetime.datetime.now()
    año_actual = now.strftime("%Y")
    año = str(año_actual)
    return año

@csrf_exempt
def verHorasExtras(request):#HorasExtras_Sin_Procesar.Estado <> %s AND 
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            ### VARIABLES
            usuario = str(json.loads(body)['usuario'])
            fecha = str(json.loads(body)['fecha'])
            #estado = '8'
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = "SELECT        CONVERT(VARCHAR(25), TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple + ' ' + TresAses_ISISPayroll.dbo.Empleados.NombresEmple) AS NOMBRE, CONVERT(VARCHAR(10), HorasExtras_Sin_Procesar.DateTimeDesde, " \
                                                "103) + ' ' + CONVERT(VARCHAR(5), HorasExtras_Sin_Procesar.DateTimeDesde, 108) + ' hs' AS DESDE, CONVERT(VARCHAR(10), HorasExtras_Sin_Procesar.DateTimeHasta, 103) + ' ' + CONVERT(VARCHAR(5), " \
                                                "HorasExtras_Sin_Procesar.DateTimeHasta, 108) + ' hs' AS HASTA, HorasExtras_Sin_Procesar.Estado AS Estado, TresAses_ISISPayroll.dbo.Empleados.CodEmpleado " \
                        "FROM            TresAses_ISISPayroll.dbo.Empleados INNER JOIN " \
                                                "HorasExtras_Sin_Procesar ON TresAses_ISISPayroll.dbo.Empleados.CodEmpleado = HorasExtras_Sin_Procesar.Legajo INNER JOIN " \
                                                "USUARIOS ON HorasExtras_Sin_Procesar.UsuarioEncargado = USUARIOS.CodEmpleado " \
                        "WHERE        (CONVERT(VARCHAR(10), HorasExtras_Sin_Procesar.FechaAlta, 103) = %s) AND (USUARIOS.Usuario = %s) " \
                        "ORDER BY TresAses_ISISPayroll.dbo.Empleados.ApellidoEmple"
                cursor.execute(sql, [fecha,usuario])
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    for row in consulta:
                        nombre = str(row[0]) + " - " + str(row[4])
                        desde = str(row[1])
                        hasta = str(row[2])
                        estado = str(row[3])
                        datos = {'Nombre': nombre, 'Desde': desde, 'Hasta': hasta, 'Estado': estado}
                        lista_data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Data': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron Horas Extras para la fecha. '})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("HorasExtras","verHorasExtras","usuario",error)
        finally:
            cursor.close()
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

@csrf_exempt
def verCargaFechasDeHorasExtras(request, mes, usuario):
    if request.method == 'GET':
        Mes = str(mes)
        User = str(usuario)
        estado = '8'
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = "SELECT DISTINCT CONVERT(VARCHAR(10), HorasExtras_Sin_Procesar.FechaAlta, 103) AS ID_FECHA, 'Fecha de Carga: ' + CONVERT(VARCHAR(5), HorasExtras_Sin_Procesar.FechaAlta, 103) AS FECHAS, HorasExtras_Sin_Procesar.FechaAlta " \
                        "FROM            HorasExtras_Sin_Procesar INNER JOIN " \
                                                "USUARIOS ON HorasExtras_Sin_Procesar.UsuarioEncargado = USUARIOS.CodEmpleado " \
                        "WHERE        (USUARIOS.Usuario = %s) AND FechaAlta >= DATEADD(DAY, -60, GETDATE()) " \
                        "ORDER BY HorasExtras_Sin_Procesar.FechaAlta DESC "
                cursor.execute(sql, [User])
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    for row in consulta:
                        idFecha = str(row[0])
                        Fecha = str(row[1])
                        datos = {'idFecha': idFecha, 'Fecha': Fecha}
                        lista_data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Data': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("HorasExtras","verCargaFechasDeHorasExtras","usuario",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['TRESASES_APLICATIVO'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    

@csrf_exempt
def busca_legajos_horas_extras(request):
    if request.method == 'POST':
        lista_data = []
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                body = request.body.decode('utf-8')
                usuario = str(json.loads(body)['usuario'])
                sql = """ 
                        SELECT DISTINCT HESP.Legajo, (EMP.ApellidoEmple + ' ' + EMP.NombresEmple) AS NOMBRE
                        FROM HorasExtras_Sin_Procesar AS  HESP INNER JOIN
                                TresAses_ISISPayroll.dbo.Empleados AS EMP ON EMP.CodEmpleado = HESP.Legajo INNER JOIN
                                USUARIOS AS US ON US.CodEmpleado = HESP.UsuarioEncargado
                        WHERE (US.Usuario = %s) AND HESP.FechaAlta >= DATEADD(DAY, -60, GETDATE()) 
                    """
                cursor.execute(sql, [usuario])
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        lista_data.append(
                            {
                                'Legajo':str(row[0]),
                                'Nombre':str(row[1])
                            }
                        )
                    return JsonResponse({'Message': 'Success', 'Data': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
@csrf_exempt
def busca_horas_extras_legajo(request):
    if request.method == 'POST':
        legajo_actual = None
        lista_data = []
        horas = []
        try:
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                body = request.body.decode('utf-8')
                legajo = str(json.loads(body)['Legajo'])
                sql = """ 
                        SELECT HESP.Legajo, (EMP.ApellidoEmple + ' ' + EMP.NombresEmple) AS NOMBRE, CONVERT(VARCHAR(10), HESP.DateTimeDesde, 
                                    103) + ' ' + CONVERT(VARCHAR(5), HESP.DateTimeDesde, 108) AS DESDE, CONVERT(VARCHAR(10), HESP.DateTimeHasta, 103) + ' ' + CONVERT(VARCHAR(5), 
                                    HESP.DateTimeHasta, 108) AS HASTA, CASE WHEN CONVERT(VARCHAR,HESP.Estado) = '8' THEN 'RECHAZADO' WHEN CONVERT(VARCHAR,HESP.Estado) = '0' THEN 'AUTORIZADO'  
                                    WHEN CONVERT(VARCHAR,HESP.Estado) = '1' THEN 'PENDIENTE' ELSE CONVERT(VARCHAR,HESP.Estado) END AS ESTADO
                        FROM HorasExtras_Sin_Procesar AS HESP INNER JOIN
                            TresAses_ISISPayroll.dbo.Empleados AS EMP ON EMP.CodEmpleado = HESP.Legajo
                        WHERE HESP.Legajo = %s AND HESP.FechaAlta >= DATEADD(DAY, -60, GETDATE()) 
                    """
                cursor.execute(sql, [legajo])
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        legajo = str(row[0])
                        nombre = str(row[1])
                        desde = str(row[2])
                        hasta = str(row[3])
                        estado = str(row[4])

                        if legajo != legajo_actual:
                            if legajo_actual is not None:
                                lista_data.append({
                                    'Legajo': legajo_actual,
                                    'Nombre': nombre_anterior,
                                    'Horas': horas
                                })
                            legajo_actual = legajo
                            nombre_anterior = nombre
                            horas = [{'Desde': desde, 'Hasta': hasta, 'Estado': estado}]
                        else:
                            horas.append({'Desde': desde, 'Hasta': hasta, 'Estado': estado})

                    if legajo_actual is not None:
                        lista_data.append({
                            'Legajo': legajo_actual,
                            'Nombre': nombre_anterior,
                            'Horas': horas
                        })
                    return JsonResponse({'Message': 'Success', 'Data': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})


















    