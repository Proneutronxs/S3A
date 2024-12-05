from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import connections
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from S3A.firebase_config import inicializar_firebase
import os
# Create your views here.


#### INICIO RENDERIZADO DE INICIO MENÚ
@login_required
def TresAses(request):
    return render (request, 'TresAses/menu/index.html')

@login_required
def verificarPermisos(request, sector):
    user_has_permission = request.user.has_perm(sector + '.puede_ingresar')
    if user_has_permission:
        if sector == 'Chacras':
            return JsonResponse ({'Message': 'Success', 'URL': 'chacras/'})
        if sector == 'Bascula':
            return JsonResponse ({'Message': 'Success', 'URL': 'bascula/'})
        if sector == 'Empaque':
            return JsonResponse ({'Message': 'Success', 'URL': 'empaque/'})
        if sector == 'RRHH':
            return JsonResponse ({'Message': 'Success', 'URL': 'rrhh/'})
        if sector == 'Frio':
            return JsonResponse ({'Message': 'Success', 'URL': 'frigorifico/'})
        if sector == 'Logistica':
            return JsonResponse ({'Message': 'Success', 'URL': 'logistica/'})
        if sector == 'Estadisticas':
            return JsonResponse ({'Message': 'Success', 'URL': 'estadisticas/'})
    return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para acceder a este sector.'})

def error_403(request, exception):
    print("Renderizado de 403")
    return render(request, 'TresAses/errores/403.html', status=403)












def funcion(request):
    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})













def push(request):
    return render (request, 'TresAses/NotiPush/subirArchivos.html')


@csrf_exempt
def recibir_archivos(request):
    if request.method == 'POST':
        try:
            archivo = request.FILES['archivo']
            parametro = request.POST.get('parametro')
            tipos_permitidos = ['text/plain', 'application/json', 'application/javascript', 'text/html']
            if archivo.content_type not in tipos_permitidos:
                return JsonResponse({'Message': 'Error', 'Nota': 'Tipo de archivo no permitido'}, status=400)

            if parametro == 'json':
                ruta_guardado = 'Applications/NotificacionesPush/archivos/'

            
            if not os.path.exists(ruta_guardado):
                os.makedirs(ruta_guardado)
            nombre_archivo = os.path.basename(archivo.name)
            ruta_completa = os.path.join(ruta_guardado, nombre_archivo)
            with open(ruta_completa, 'wb+') as destino:
                for chunk in archivo.chunks():
                    destino.write(chunk)

            #inicializar_firebase()

            return JsonResponse({'Message': 'Success', 'Nota': 'Archivo subido correctamente'})
        except Exception as e:
            return JsonResponse({'Message': 'Error', 'Nota': str(e)}, status=500)
    else:
        return JsonResponse({'Message': 'No se pudo resolver la petición.'}) 
