from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from S3A.funcionesGenerales import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import datetime 

# Create your views here.
@login_required
def Logistica(request):
    return render (request, 'Logistica/logistica.html')

@login_required
def seguimientoViajes(request):
    return render (request, 'Logistica/Seguimiento/seguimientoViajes.html')