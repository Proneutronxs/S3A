
from django.views.decorators.csrf import csrf_exempt
from S3A.funcionesGenerales import *
from django.views.static import serve
from django.db import connections
from django.http import JsonResponse
from django.http import HttpResponse, Http404
import json
import math
import os






def chacras_filas_qr(request,usuario):
    if request.method == 'GET':
        values = [str(usuario)]
        try:
            lista_data = []
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                lista_chacras = listado_Chacras(values)
                sql = """ 
                        EXEC SP_SELECT_CHACRAS_FILAS_QR %s
                    """
                cursor.execute(sql,values)
                consulta = cursor.fetchall()
                if consulta:
                    for row in consulta:
                        lista_data.append({
                            "ID_PRODUCTOR": row[0],
                            "PRODUCTOR": row[1],
                            "ID_CHACRA": row[2],
                            "CHACRA": row[3],
                            "ID_FILA": row[4],
                            "ID_CUADRO": row[5],
                            "CUADRO": row[6],
                            "ID_VARIEDAD": row[7],
                            "ID_QR": row[8],
                            "QR": row[9],
                            "TIPO_QR": row[10],
                            "TEMPORADA_QR": row[11],
                            "ALTA_QR": row[12],
                            "ESTADO_QR": row[13],
                            "ACTIVIDAD_QR": row[14],
                            "VALOR_REFERENCIA": row[15],
                            "AÑO_PLANTACION": row[16],
                            "NRO_PLANTAS": row[17],
                            "DIST_FILAS": row[18],
                            "DIST_PLANTAS": row[19],
                            "SUPERFICIE": row[20],
                            "ESTADO_FILA": row[21],
                            "VARIEDAD": row[22],
                            "V_PODA":row[23],
                            "V_RALEO":row[24]
                        })
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data, 'Chacras':lista_chacras})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': error})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    

def listado_Chacras(values):
    listado_chacras = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            sql = """ 
                    SELECT CH.IdChacra AS ID_CHACRA, RTRIM(CH.Nombre) AS CHACRA, CH.IdProductor AS ID_PRODUCTOR, RTRIM(PR.Nombre) AS PRODUCTOR
                    FROM S3A.dbo.Chacra AS CH INNER JOIN
                        S3A.dbo.Productor AS PR ON PR.IdProductor = CH.IdProductor
                    WHERE CH.IdChacra IN (SELECT valor FROM dbo.fn_Split((SELECT Chacras FROM USUARIOS WHERE Usuario = %s), ','))
                    ORDER BY RTRIM(CH.Nombre)
                """
            cursor.execute(sql,values)
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    listado_chacras.append({
                        "ID_CHACRA":row[0],
                        "CHACRA":row[1],
                        "ID_PRODUCTOR":row[2],
                        "PRODUCTOR":row[3]
                    })
            return listado_chacras
    except Exception as e:
        registroRealizado(values,"LISTADO_CHACRAS",str(e))
        return listado_chacras