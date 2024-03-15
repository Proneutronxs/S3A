from django.urls import path
from Applications.Logistica import views
from Applications.Logistica.folderViews.SeguimientosViajes import seguimientos

urlpatterns = [

    # ### SOLO RENDERIZADO
    path('', views.Logistica, name="logistica"),
    
    path('seguimiento-viajes/', views.seguimientoViajes, name="seguimiento_viajes"),

    path('horas-extras/', views.horasExtras, name="horas_extras_logistica"),

    path('horas-extras/autoriza', views.horasExtras_autoriza, name="horas_extras_logistica_autoriza"),

    ### INICIO JAVA SCRIPT SEGUIMIENTOS ###

    path('seguimiento-viajes/listado-choferes/', seguimientos.listadoChofer, name="listado_chofer"),

    path('seguimiento-viajes/listado-viajes/', seguimientos.listadoViajes, name="listado_viajes"),

    path('seguimiento-viajes/listado-asignados/', seguimientos.listadoAsignados, name="listado_asignados"),

    path('seguimiento-viajes/listado-rechazados/', seguimientos.listadoRechazados, name="listado_rechazados"),

    path('seguimiento-viajes/guarda-vacios/', seguimientos.asignaViajeActualizaVacios, name="asigna_viajes_vacios"),

    path('seguimiento-viajes/elimina-rechazado/idAsignacion=<str:idAsignacion>', seguimientos.eliminaRechazado, name="elimina_rechazado"),

    ### FINAL JAVA SCRIPT SEGUIMIENTOS ###

    ### HORAS EXTRAS LOGISTICA ###

    path('horas-extras/autoriza/carga-combox-cc', views.cargaCentrosEmpaque, name="centros_logistica_autoriza"),

    path('horas-extras/autoriza/ver-horas-extras', views.mostrarHorasCargadasPorCC, name='ver_horas_extras_logistica'),

    path('horas-extras/autoriza/horas-extras', views.autorizaHorasCargadas, name='autoriza_horas_extras_logistica'),

    path('horas-extras/autoriza/elimina/horas-extras', views.eliminaHorasSeleccionadas, name='elimina_horas_extras_logistica'),

    path('horas-extras/ver', views.verHorasExtras, name='ver_horas_extras_logistica'),

    path('horas-extras/ver/listado-horas', views.listadoHorasExtrasEstadoL, name='listado_horas_extras_estado_logistica'),

    path('horas-extras/ver/restaura-horas', views.restauraHoraL, name='restaura_horas_logistica'),

    path('horas-extras/ver/exportar-excel', views.creaExcelHorasMostradas, name='exporta_excel_horas_logistica'),


]