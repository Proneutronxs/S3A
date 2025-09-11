from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from S3A.funcionesGenerales import *
from S3A.conexionessql import *
import json
from Applications.Mobile.GeneralApp.archivosGenerales import insertaRegistro
from django.db import connections
from django.http import JsonResponse

# Create your views here.

###  METODO POST PARA PODER INSERTAR LAS FICHADAS EN EL SQL
@csrf_exempt
def insert_fichada(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            usuario = str(json.loads(body)['usuario'])
            fechaHora = str(json.loads(body)['actual'])
            registro = str(json.loads(body)['registro'])
            datos = json.loads(body)['Data']
            debug_error(usuario,datos,"")
            registroRealizado(usuario,"FC",datos)
            with connections['principal'].cursor() as cursor:
                for item in datos:
                    legajo = item['Legajo'] ### LEGAJO
                    tarjeta = traeLegTarjeta(str(item['Codigo']), str(item['Tarjeta']))### TARJETA
                    fecha = item['Fecha'] ### FECHA
                    hora = item['Hora'] ### HORA 
                    tipo = item['Tipo'] ### E para ENTRADA y S para SALIDA
                    nodo = item['Nodo'] ### NODO HACE REFERENCIA A SALIDA O ENTRADA (RELOJ-ID)
                    codigo = item['Codigo'] ### CODIGO HACE REFERENCIA AL ID DONDE SE REGISTRO EL LEGAJO
                    simulacion = "1" ### DATO SIEMPRE EN 1
                    estado = "0"  ### DATO SIEMPRE EN 0
                    orden = "3" ### DATO VARIABLE 0 O 3
                    sql = "INSERT INTO T_Fichadas (ficTarjeta, ficFecha, ficHora, ficES12, ficNodo, ficSimulacion, legCodigo, ficEstado, ficOrden) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    values = (tarjeta, fecha, hora, tipo, nodo, simulacion, codigo, estado, orden)
                    cursor.execute(sql, values)
            nota = "Los registros se guardaron exitosamente."
            est = "E"
            insertaRegistro(usuario,fechaHora,registro,est)
            return JsonResponse({'Message': 'Success', 'Nota': nota})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("Presentismo","insert_fichadas","usuario",error)
            est = "F"
            insertaRegistro(usuario,fechaHora,registro,est)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
def traeLegTarjeta(legCodigo, legTarjeta):
    try:
        with connections['principal'].cursor() as cursor:
            sql = """ SELECT legTarjeta FROM T_Legajos WHERE legCodigo = %s """
            cursor.execute(sql, [legCodigo])
            consulta = cursor.fetchone()
            if consulta:
                numTarjeta = str(consulta[0])
                return numTarjeta
            else:
                return legTarjeta
    except Exception as e:
        error = str(e)
        debug_error(legCodigo,"",error)
        return error

@csrf_exempt
def data(request):
    #DATA
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            data = json.loads(body)
            print(data)
            nota = "Visualización Correcta"
            return JsonResponse({'Message': 'Success', 'Nota': nota})
        except json.JSONDecodeError as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    



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
