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
            body = request.body.decode('utf-8')
            datos = json.loads(body)['Data']
            for item in datos:
                Legajo = item['Legajo'] ### LEGAJO
                Regis_Epl = item['Regis_Epl']### ID LEGAJO
                Desde = item['DateTimeDesde'] ### DATETIME DESDE
                Hasta = item['DateTimeHasta'] ### DATETIME HASTA
                idMotivo = item['Motivo'] ### MOTIVO
                Descripcion = item['Descripcion'] ### DESCRIPCION DE LA TAREA
                Arreglo = item['Arreglo'] ### SI SE HIZO UN ARREGLO CON RESPECTO A LA HORA
                Usuario = item['Usuario'] ### USUARIO DE LA APLICACIÓN
                Autorizado = item['Autorizado'] ### RELACIONAR EL LEGAJO O BIEN CARGAR EL ID DEL AUTORIZADO
                EstadoPreCarga = "1" ### ESTADO PRE CARGA SIEMPRE EN 1 

                #with connections['default'].cursor() as cursor:
                    #sql = "INSERT INTO PRE_CARGA_HE (CodEmpleado, Regis_Epl, ApellidoNombre, Desde, Hasta, idMotivo, DescripcionTarea, EstadoPreCarga, ficOrden) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    #values = (CodEmpleado, Regis_Epl, Nombre_Apellido, Desde, Hasta, idMotivo, Descripcion, Autorizado, EstadoPreCarga)
                    #cursor.execute(sql, values)            

                print(Legajo + " - " + Regis_Epl +  " - " + Desde + " - " + Hasta +  " - " + Arreglo + " - " + idMotivo + " - " + Descripcion + " - " + Autorizado + " - " + EstadoPreCarga + " - " + Usuario)
            nota = "Los Horas Extras se envíaron correctamente."
            return JsonResponse({'Message': 'Success', 'Nota': nota})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})


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