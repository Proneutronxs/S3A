from django.urls import path
from Applications.Inicio import views

urlpatterns = [

    ### SOLO RENDERIZADO
    path('', views.inicioSesion, name="inicio_sesion"),



]