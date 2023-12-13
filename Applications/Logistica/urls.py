from django.urls import path
from Applications.Logistica import views
from Applications.Logistica.folderViews.SeguimientosViajes import seguimientos

urlpatterns = [

    # ### SOLO RENDERIZADO
    path('', views.Logistica, name="logistica"),
    path('seguimiento-viajes/', views.seguimientoViajes, name="seguimiento_viajes"),

    ### INICIO JAVA SCRIPT SEGUIMIENTOS ###

    path('seguimiento-viajes/listado-choferes/', seguimientos.listadoChofer, name="listado_chofer"),

    path('seguimiento-viajes/listado-viajes/', seguimientos.listadoViajes, name="listado_viajes"),

    path('seguimiento-viajes/listado-asignados/', seguimientos.listadoAsignados, name="listado_asignados"),

    path('seguimiento-viajes/listado-rechazados/', seguimientos.listadoRechazados, name="listado_rechazados"),

    ### FINAL JAVA SCRIPT SEGUIMIENTOS ###



]