from django.urls import path
from Applications.Api import views
from Applications.Api.vistas.CRC import demoCRC
from Applications.Api.vistas.FruitTruck import fruit
from Applications.Api.vistas.Sipreta import sipreta
from S3A.funcionesGenerales import *


urlpatterns = [

    path('data-general/', demoCRC.dataGeneral, name="data-general-api"),

    path('data-general/with-crc/', demoCRC.dataConCRC, name="data_general_api_con_crc"),

    path('data-general/ultimo-remito/', demoCRC.crc_ultimo_remito, name="crc_ultimo_remito"),

    path('data-general/sim-remito/', demoCRC.tabla_sim_remito, name="tabla_sim_remito"),
    


    ### CAMIONES APLICACION DE FRUIT TRUCK ###

    path('fruit/listar-transporte/', fruit.listarTransporte, name="fruit_choferes_listar_transportes"),

    path('fruit/listar-transporte/datos-transportes/', fruit.listarDataTransporte, name="fruit_choferes_listar_transportes_data_transportes"),

    path('fruit/listar-transporte/insertar-transporte/', fruit.guardar_transporte_chofer, name="fruit_guardar_transporte_chofer"),


    ### SOLICITUD DE VIAJES ###

    path('fruit/listar-viaje/chofer=<str:ID_CA>/', fruit.Obtener_Viaje_Chacras, name="fruit_obtener_viajes_chacras"),

    path('fruit/listar-viaje-aceptado/chofer=<str:ID_CA>/', fruit.Obtener_Viaje_Aceptado, name="fruit_obtener_viajes_aceptado"),

    path('fruit/rechaza-acepta-viaje/', fruit.acepta_rechaza_viaje, name="fruit_acepta_rechaza_viaje"),

    ### CAMBIA ESTADOS DE CHOFER ###

    path('fruit/estado-chofer/cambia-estado/', fruit.cambia_estado_chofer, name="fruit_cambia_estado_chofer"),

    ### BUSQUEDA Y DESCARGA DE REMITOS###

    path('fruit/listar-remitos/buscar/', fruit.mostrar_remitos_fecha_chofer, name="fruit_mostrar_remitos_fecha_chofer"),

    path('fruit/descarga-remito/remito=<str:ID_REMITO>/', fruit.crear_remito_ID, name="fruit_crear_remito_ID"),

    path('fruit/descarga-remito/nombre=<str:nombreRemito>/', fruit.descargar_pdf, name="fruit_descargar_pdf"),

    ### SERVICIO Y FINALIZACIÓN ###

    path('fruit/servicio-finaliza/', fruit.servicio_finalizacion, name="fruit_servicio_finalizacion"),

    ### SERVICIO NOTIFICACIÓN RECIBIDA ###

    path('fruit/notificacion-recibida/', fruit.actualiza_notificacion_recibida, name="fruit_actualiza_notificacion_recibida"),

    ### ACTUALIZACION DE DESTINOS

    path('fruit/listar-nuevos-destinos/chofer=<str:ID_CA>/', fruit.Obtener_Nuevos_destinos, name="fruit_obtener_viajes_chacras"),

    ### LISTADO DE VIAJES

    path('fruit/listar-viajes/', fruit.listado_asignados, name="fruit_listado_asignados"),

    path('fruit/servicio-fcs/', fruit.servicio_fcs_online, name="servicio_fcs_online"),  


    ############ ON LINE ###################


    ################ SIPRETA ######################

    path('sipreta/data-chacras-filas/usuario=<str:usuario>', sipreta.chacras_filas_qr, name="sipreta_chacras_filas_qr"),  

    path('sipreta/data-sync-all/', sipreta.data_sync_all, name="sipreta_data_sync_all"),  




]