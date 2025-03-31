from openpyxl.styles import PatternFill, Font, Border, Side
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib.auth.decorators import login_required
from S3A.funcionesGenerales import obtenerHorasArchivo, registroRealizado
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


# Create your views here.

@login_required
def Md_Rrhh(request):
    user_has_permission = request.user.has_perm('Md_Rrhh.puede_ingresar')
    if user_has_permission:
        return render (request, 'Md_Rrhh/index.html')
    return render (request, 'Md_Rrhh/404.html')

@login_required
def Archivo_Isis(request):
    user_has_permission = request.user.has_perm('Md_Rrhh.puede_ingresar')
    if user_has_permission:
        return render (request, 'Md_Rrhh/HorasExtras/archivo_isis.html')
    return render (request, 'Md_Rrhh/404.html')









def descarga_archivo_excel(request, filename):
    nombre = filename
    filename = 'Applications/Md_Rrhh/Archivos/Excel/' + filename
    if os.path.exists(filename):
        response = serve(request, os.path.basename(filename), os.path.dirname(filename))
        response['Content-Disposition'] = f'attachment; filename="{nombre}"'
        return response
    else:
        raise 
    
@csrf_exempt    
def data_listado_horas_extras_isis(request):
    if not request.user.is_authenticated:
        return JsonResponse({'Message': 'Not Authenticated', 'Redirect': '/'})
    if request.method == 'POST':
        user_has_permission = request.user.has_perm('Md_Rrhh.puede_ver')
        if user_has_permission:
            try:
                inicio = str(request.POST.get('Incio'))
                final = str(request.POST.get('Final'))
                archivo = str(request.POST.get('Archivo'))
                values = [inicio,final]
                lista_data = jsonArchivoIsis(values)
                if lista_data:
                    if archivo == "N":
                        return JsonResponse({'Message': 'Success', 'Datos': lista_data})  
                    # else:
                    #     excel_response = general_excel_horas_extras(lista_data)            
                    #     return excel_response 
                else:
                    data = 'No se encontraron datos.'
                    return JsonResponse({'Message': 'Error', 'Nota': data})
            except Exception as e:
                data = str(e)
                return JsonResponse({'Message': 'Error', 'Nota': data})
        else:
            return JsonResponse ({'Message': 'Error', 'Nota': 'No tiene permisos para resolver la petición.'})
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'})

def jsonArchivoIsis(values):
    lista_data = []
    try:
        with connections['S3A'].cursor() as cursor:
            cursor.execute('EXEC MDR_LISTADO_ARCHIVO_ISIS %s,%s', values)
            consulta = cursor.fetchall()
            if consulta:
                for row in consulta:
                    lista_data.append({
                        'Legajo':str(row[0]), 
                        'Horas50':str(row[1]), 
                        'Cod50':str(row[2]), 
                        'Horas100':str(row[3]), 
                        'Cod100':str(row[4]), 
                        'HorasS':str(row[5]), 
                        'CodS':str(row[6]), 
                        'Ac50':str(row[7]), 
                        'Ac100':str(row[8]), 
                        'Sindicato':str(row[9]), 
                        'Nombre':str(row[10]), 
                        'Centro':str(row[11])
                    })
                return lista_data 
            else:
                return lista_data
    except Exception as e:
        return lista_data









































































