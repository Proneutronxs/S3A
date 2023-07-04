from django.urls import path
from Applications.Mobile.HorasExtras import views

urlpatterns = [

    ### CARGA Y MUESTRA LOS MOTIVOS PARA SELECCIONAR EL MOTIVO PARA LAS HORAS EXTRAS
    path('mostrar/motivos/horasextras', views.motrar_MotivosHE, name="mostrar_MotivosHorasExtras"),

    ### INSERTA LAS HORAS EXTRAS ENVÍADAS HORAS EXTRAS A AUTORIZAR (POST BODY REQUEST)
    path('inserta/horasextras', views.insert_HoraExtra, name="inserta_horasExtras"),

    ### MUESTRA HORAS EXTRAS ACTIVAS - PETICIONES DE HORAS EXTRAS (GET BODY REQUEST)
    path('mostrar/horasextras/activas', views.mostrarHoraExtrasActivas, name="muestra_horasExtras_activas"),

    ### GUARDA LAS HORAS EXTRAS EN S3A UBICACIÓN Y CONCATENACIÓN CON EL ID (ACTUALIZA EL ESTADO DE LA PETICIÓN)
    path('inserta/horasextras/s3a', views.enviarHorasExtras, name="envia_horasExtras_s3a."),


]