from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from S3A.funcionesGenerales import *
from django.views.static import serve
from Applications.ModelosPDF.remitoChacra import *
from Applications.Mobile.FletesRemitos.views import actualizaNombrePDF
from django.db import connections
from django.http import JsonResponse
from django.http import HttpResponse, Http404
import os


# Create your views here.


@login_required
@permission_required('Chacras.puede_ingresar', raise_exception=True)
def Chacras(request):
    return render (request, 'Chacras/chacras.html')


@login_required
def planillas(request):
    return render (request, 'Chacras/Planillas/planillas.html')

@login_required
def general(request):
    return render (request, 'Chacras/Planillas/general.html')