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


    ############### PEDIDOS DE FLETE ################


    path('pedidos-flete/', views.pedidos_flete, name='pedidos_flete'),

    path('pedidos-flete/asignacion/', views.asignacion_pedidos_flete, name='asignacion_pedidos_flete'),

    path('pedidos-flete/asignacion/listar-pendientes/', views.mostrar_pedidos_flete, name='mostrar_pedidos_flete_pendientes'),

    path('pedidos-flete/asignacion/listar-asignados/', views.mostrar_pedidos_flete, name='mostrar_pedidos_flete_asignados'),

    path('pedidos-flete/asignacion/mostrar-detalles/', views.mostrar_detalles_pedido_flete, name='mostrar_detalles_pedido_flete'),

    path('pedidos-flete/asignacion/viaje-detalles/', views.detalles_de_viajes_activos, name='detalles_de_viajes_activos'),

    path('pedidos-flete/asignacion/listar-choferes/', views.mostrar_choferes, name='mostrar_choferes'),

    path('pedidos-flete/asignacion/mapeo-ultima-ubicacion/', views.mapeo_Ultima_Ubicacion, name='mapeo_Ultima_Ubicacion'),

    path('pedidos-flete/baja-pedidos/', views.baja_pedidos_flete, name='baja_pedidos_flete'),


]