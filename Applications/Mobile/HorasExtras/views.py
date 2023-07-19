from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from S3A.conexionessql import *
from datetime import datetime
import json

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
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

###  METODO POST PARA PODER INSERTAR LAS HORAS EXTRAS PRE AUTORIZADAS EN EL SQL (BODY)
@csrf_exempt
def insert_HoraExtra(request):
    if request.method == 'POST':
        try:
            lista_tieneHE_asignada = []
            body = request.body.decode('utf-8')
            datos = json.loads(body)['Data']
            for item in datos:
                Legajo = str(item['Legajo']) ### LEGAJO
                Regis_Epl = str(item['Regis_Epl'])### ID LEGAJO
                Desde = str(item['DateTimeDesde']) ### DATETIME DESDE
                Hasta = str(item['DateTimeHasta']) ### DATETIME HASTA
                idMotivo = str(item['Motivo']) ### MOTIVO
                Descripcion = str(item['Descripcion']) ### DESCRIPCION DE LA TAREA
                Arreglo = str(item['Arreglo']) ### SI SE HIZO UN ARREGLO CON RESPECTO A LA HORA
                Usuario = str(item['Usuario']) ### USUARIO DE LA APLICACIÓN
                Autorizado = str(item['Autorizado']) ### RELACIONAR EL LEGAJO O BIEN CARGAR EL ID DEL AUTORIZADO
                Estado = "1" ### ESTADO PRE CARGA SIEMPRE EN 1 
                
                horaDesde, horaHasta = retornaHHMM(Desde,Hasta)
                fechaDesde, fechaHasta = retornaYYYYMMDD(Desde,Hasta)
                print(horaDesde,horaHasta,fechaDesde,fechaHasta)

                if verificaHoraExtra(horaDesde, horaHasta, fechaDesde, fechaHasta):
                    lista_tieneHE_asignada.append(Legajo)
                else:
                    with connections['default'].cursor() as cursor:
                        sql = "INSERT INTO HorasExtras_Sin_Procesar (Legajo, Regis_Epl, DateTimeDesde, DateTimeHasta, IdMotivo, DescripcionMotivo, Arreglo, UsuarioEncargado, Autorizado, Estado) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                        values = (Legajo, Regis_Epl, Desde, Hasta, idMotivo, Descripcion, Arreglo, Usuario, Autorizado, Estado)
                        cursor.execute(sql, values)            
                        cursor.close()
            if len(lista_tieneHE_asignada) == 0:
                nota = "Los Horas Extras se envíaron correctamente."
                return JsonResponse({'Message': 'Success', 'Nota': nota})
            else:
                nombres = []
                for legajo in lista_tieneHE_asignada:
                    Apellido = traeApellidos(str(legajo))
                    nombres.append(Apellido)
                nota = "Los siguientes Apellidos ya tienen asignadas horas extras en ese rango horario: \n" + ', \n'.join(nombres) + '.'
                return JsonResponse({'Message': 'Success', 'Nota': nota})
        except Exception as e:
            print(e)
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['default'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

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
def retornaYYYYMMDD(f1,f2):
    formato_entrada = "%Y-%m-%dT%H:%M:%S.%f"
    formato_salida = "%Y-%m-%d"
    fechaUno = datetime.strptime(f1, formato_entrada)
    fechaDos = datetime.strptime(f2, formato_entrada)
    fechaDesde = fechaUno.strftime(formato_salida)
    fechaHasta = fechaDos.strftime(formato_salida)
    return fechaDesde, fechaHasta

def verificaHoraExtra(horaDesde,horaHasta,fechaDesde,fechaHasta):
    try:
        with connections['default'].cursor() as cursor:
            sql = "SELECT  CONVERT(VARCHAR(5), DateTimeDesde, 108) AS H_DESDE, CONVERT(VARCHAR(5), DateTimeHasta, 108) AS H_HASTA "\
                    "FROM HorasExtras_Sin_Procesar " \
                    "WHERE TRY_CONVERT(DATE, DateTimeDesde) >= %s AND TRY_CONVERT(DATE, DateTimeHasta) <= %s"
            cursor.execute(sql, [fechaDesde, fechaHasta])
            consulta = cursor.fetchone()
            if consulta:
                horaD = str(consulta[0])
                horaH =str(consulta[1])
                if verificar_solapamiento(horaDesde,horaHasta,horaD,horaH):
                    return True
                else:
                    return False
            else:
                return False
    except Exception as e:
        error = str(e)
        return error
    finally:
        connections['default'].close()

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
        return error
    finally:
        connections['ISISPayroll'].close()

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
            with connections['default'].cursor() as cursor:
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
            with connections['default'].cursor() as cursor:
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