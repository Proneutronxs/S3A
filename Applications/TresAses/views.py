from django.shortcuts import render

from django.db import connections
from django.http import JsonResponse
# Create your views here.


#### INICIO RENDERIZADO DE INICIO MENÚ

def TresAses(request):
    return render (request, 'TresAses/menu/index.html')



def funcion(request):
    return JsonResponse({'Message': 'Not Found', 'Nota': 'No se encontraron datos.'})














