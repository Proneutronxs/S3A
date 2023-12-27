from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db import connections
from django.http import HttpResponseForbidden
from django.http import JsonResponse
# Create your views here.


#### INICIO RENDERIZADO DE INICIO MENÚ
@login_required
def TresAses(request):
    return render (request, 'TresAses/menu/index.html')

@login_required
def verificarPermisos(request, sector):
    user_has_permission = request.user.has_perm(sector + '.puede_ingresar')
    if user_has_permission:
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
    return JsonResponse ({'Message': 'Not Found', 'Nota': 'No tiene permisos para acceder a este sector.'})

def error_403(request, exception):
    print("Renderizado de 403")
    return render(request, 'TresAses/errores/403.html', status=403)












def funcion(request):
    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})














