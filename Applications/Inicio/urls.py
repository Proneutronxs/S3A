from django.urls import path
from Applications.Inicio import views

urlpatterns = [

    ### SOLO RENDERIZADO
    path('', views.inicioSesion, name="inicio_sesion"),

    path('accounts/login/login-3A/', views.custom_login, name='login-3A'),



]