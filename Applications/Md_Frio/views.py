from openpyxl.styles import PatternFill, Font, Border, Side
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from S3A.funcionesGenerales import Centros_Modulos_Usuarios
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden
from openpyxl.drawing.image import Image
from django.views.static import serve
from openpyxl.styles import Alignment
from django.shortcuts import render
from django.db import connections
from datetime import datetime
from io import BytesIO
import pandas as pd
import os


### RENDERIZADO

@login_required
def Md_Frio(request):
    user_has_permission = request.user.has_perm('Md_Frio.puede_ingresar')
    if user_has_permission:
        return render (request, 'Md_Frio/index.html')
    return render (request, 'Md_Frio/404.html')

@login_required
def Autoriza_Horas_Extras(request):
    user_has_permission = request.user.has_perm('Md_Frio.puede_ingresar')
    if user_has_permission:
        return render (request, 'Md_Frio/HorasExtras/autoriza.html')
    return render (request, 'Md_Frio/404.html')




### PETICIONES REQUEST      EXEC GENERAL_PERSONAL_HORAS_EXTRAS '2025-01-01', '2025-03-31', '', '', 'CENTROS-FRIO'

def Centros_por_Usuario(request):
    if request.method == 'GET':
        usuario = str(request.user).upper()
        try:
            listado_data = Centros_Modulos_Usuarios("CENTROS-FRIO",usuario)
            listado_estados = [{'IdEstado':'', 'Descripcion':'TODO'},{'IdEstado':'0', 'Descripcion':'AUTORIZADO'},{'IdEstado':'3', 'Descripcion':'PENDIENTE'},{'IdEstado':'8', 'Descripcion':'ELIMINADO'}]
            if listado_data:
                return JsonResponse({'Message': 'Success', 'Datos': listado_data, 'Estados':listado_estados})
            else:
                data = "No se encontraron Centros de Costos Asignados."
                return JsonResponse({'Message': 'Error', 'Nota': data})                
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        data = "No se pudo resolver la Petición"
        return JsonResponse({'Message': 'Error', 'Nota': data})

@csrf_exempt
def combox_lista_personal_horas_extras(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Message': 'Not Authenticated', 'Redirect': '/'})
    if request.method == 'POST':
        try:
            inicio = str(request.POST.get('Inicio'))
            final = str(request.POST.get('Final'))
            centro = str(request.POST.get('Centro'))
            usuario = str(request.user).upper()
            codigo = 'CENTROS-FRIO'
            values = [inicio,final,centro,usuario,codigo]
            with connections['TRESASES_APLICATIVO'].cursor() as cursor:
                sql = """ 
                        EXEC GENERAL_PERSONAL_HORAS_EXTRAS %s, %s, %s, %s, %s
                    """
                cursor.execute(sql, values)
                consulta = cursor.fetchall()
                if consulta:
                    lista_data = [{'Legajo': '', 'Nombre':'TODOS'}]
                    for row in consulta:
                        lista_data.append({
                            'Legajo': str(row[0]), 
                            'Nombre': str(row[1])
                        })
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data})
                else:
                    data = "No se encontraron Datos."
                    return JsonResponse({'Message': 'Error', 'Nota': data})
        except Exception as e:
            data = str(e)
            return JsonResponse({'Message': 'Error', 'Nota': data})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
@csrf_exempt
def data_listado_horas_extras(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Message': 'Not Authenticated', 'Redirect': '/'})
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Md_Frio.puede_ver')
        if user_has_permission:
            try:
                inicio = str(request.POST.get('Inicio'))
                final = str(request.POST.get('Final'))
                estado = str(request.POST.get('Estado'))
                legajo = str(request.POST.get('Legajo'))
                centro = str(request.POST.get('Centro'))
                usuario = str(request.user).upper()
                codigo = 'CENTROS-FRIO'
                values = [inicio,final,estado,legajo,centro,usuario,codigo]
                lista_data = jsonListadoHorasEstras(values)
                if lista_data:
                    return JsonResponse({'Message': 'Success', 'Datos': lista_data})  
                else:
                    data = 'No se pudo cargar los datos.'
                    return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})
    
def jsonListadoHorasEstras(values):
    lista_data = []
    try:
        with connections['TRESASES_APLICATIVO'].cursor() as cursor:
            cursor.execute('EXEC MDG_LISTADO_HORAS_EXTRAS %s,%s,%s,%s,%s,%s,%s', values)
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    lista_data.append({
                        'ID_HEP':str(row[0]), 
                        'Legajo':str(row[1]), 
                        'Nombre':str(row[2]),  
                        'Desde':str(row[3]), 
                        'Hasta':str(row[4]), 
                        'Motivo':str(row[5]), 
                        'Descripcion':str(row[6]), 
                        'Cantidad':str(row[7]), 
                        'Autoriza':str(row[8]), 
                        'Centro':str(row[9]), 
                        'Solicita':str(row[10]), 
                        'Estado':str(row[11]), 
                        'Tipo':str(row[12]),
                        'E':str(row[13])
                    })
                return lista_data 
            else:
                return lista_data
    except Exception as e:
        return lista_data









































