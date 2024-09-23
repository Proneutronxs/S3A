from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from S3A.funcionesGenerales import *
from django.views.static import serve
from django.db import connections
from django.http import JsonResponse
from django.http import HttpResponse, Http404
import os

@csrf_exempt
def dataGeneral(request):
    if request.method == 'POST':
        desde = request.POST.get('Inicio')
        hasta = request.POST.get('Final')
        try:
            with connections['S3A'].cursor() as cursor:
                sql = """ 

                    """
                cursor.execute(sql, [desde,hasta])
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = []
                    for row in consulta:
                        legajo = str(row[0])
                        nombre = str(row[1])
                        datos = {'Legajo': legajo, 'Nombre': nombre}
                        lista_data.append(datos)
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data})
                else:
                    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})
        except Exception as e:
            error = str(e)
            insertar_registro_error_sql("GeneralApp","personal_por_Ccostos_asistencia","usuario",error)
            return JsonResponse({'Message': 'Error', 'Nota': error})
        finally:
            connections['S3A'].close()
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})