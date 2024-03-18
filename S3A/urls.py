"""S3A URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Applications.Inicio import views
from django.contrib.auth.views import logout_then_login

urlpatterns = [

    ### ADMINISTRACION DE PANEL DJANGO
    path('administracion/sistemas/Django', admin.site.urls),

    ### API GENERAL APPLICATIONS
    path('api/general/', include('Applications.Mobile.GeneralApp.urls')),

    #### MOBILE PRESENTISMO
    path('api/presentismo/', include('Applications.Mobile.Presentismo.urls')),

    #### MOBILE ANTICIPOS
    path('api/anticipos/', include('Applications.Mobile.Anticipos.urls')),

    #### MOBILE HORAS EXTRAS
    path('api/hextras/', include('Applications.Mobile.HorasExtras.urls')),

    #### MOBILE REMITOS - FLETES - PRE CARGA INGRESO BASCULA
    path('api/fletes-remitos/', include('Applications.Mobile.FletesRemitos.urls')),

    ### URL APLICACIÓN TRES ASES GENERAL
    path('', include('Applications.TresAses.urls')),

    path('bascula/', include('Applications.Bascula.urls')),

    path('rrhh/', include('Applications.RRHH.urls')),

    path('empaque/', include('Applications.Empaque.urls')),

    path('frigorifico/', include('Applications.Frio.urls')),

    path('logistica/', include('Applications.Logistica.urls')),

    path('reportes/', include('Applications.Reportes.urls')),

    path('estadisticas/', include('Applications.Estadisticas.urls')),

    path('login/', include('Applications.Inicio.urls')),

    path('accounts/login/', views.inicioSesion, name="inicio_sesion"),

    path('accounts/login/login-3A/', views.custom_login, name='login-3A'),

    path('accounts/login/change-password/', views.cambiar_password, name='change_password'),

    path('logout/', logout_then_login, name='logout'),

    path('accounts/login/logout/', logout_then_login, name='log_out'),
]
