from django.urls import path
from Applications.Mobile.FletesRemitos import views

urlpatterns = [
   
   ### DATA INICIAL PARA PEDIDO DE FLETES
   path('data-inicial', views.datos_Iniciales_Flete, name="data_inicial"),

   ## DATA INICIAL PARA PEDIDO DE FLETES -- PRODUCTORES
   path('data-inicial/productores', views.datos_Iniciales_Flete_Productores, name="data_inicial_productores"),

   ### DATA SEGUN ID DE PRODUCTOR
   path('data-productor/idProductor=<str:idProductor>', views.idProductor_Chacra, name="idProductor_Chacra_Zona"),

   ### DATA ZONA SEGUN ID PRODUCTO Y ID CHACRA
   path('data-zona/idProductor=<str:idProductor>&idChacra=<str:idChacra>', views.idProductor_Zona, name="idProductor_Zona"),

   ### DATA SEGUN ID DE ESPECIE
   path('data-especie/idEspecie=<str:idEspecie>', views.idEspecie_Varierad, name="idEspecie_Variedad"),

   ### METODO POST INSERTA PEDIDO DE FLETE
   path('data-inserta/pedido-flete', views.insertaPedidoFlete, name="inserta_Pedido_Flete"),

   ### DATA MUESTRA ASIGNACIONES PENDIENTES
   path('data-asignaciones/usuario=<str:usuario>', views.llamaAsignacionesPendientes, name="llama_asignaciones_pendientes"),

   ## DATA MUESTRA DATOS DE LA ASIGNACION SELECCIONADA POR EL ID DE LA ASIGNACION
   path('data-asignacion/idAsignacion=<str:idAsignacion>', views.llamaDataAsignacionPendiente, name="llama_data_asignacion_pendiente"),

   ### METODO POST DE CRACIÓN DE REMITOS
   path('data-inserta-crea/remitos', views.insertCreaciónRemitos, name="inserta_Crea_Remitos"),

   ### DATA MUESTRA LISTADO DE REMITOS
   path('data-listado-remitos/chofer=<str:chofer>', views.mostrarListadoRemitos, name="motrar_listado_remitos"),

   ### METODO DESCARGAR PDF
   path('data-descargar-remito/<str:filename>', views.descarga_pdf_remito_chacra, name="descarga_pdf_remito_chacra"),

   ### METODO VER PDF
   path('data-ver-remito/<str:filename>', views.ver_pdf_remito_chacra, name="ver_pdf_remito_chacra"),

   ### METODO VER VIAJES ASIGNADOS POR CHOFER
   path('data-ver-viajes/chofer=<str:chofer>', views.listadoViajesAsignados, name="listado_viajes_asignados"),

   ### METODO ACEPTA RECHAZA VIAJE
   path('data-acepta-rechaza/isAsignacion=<str:idAsignacion>&chofer=<str:chofer>&acepta=<str:acepta>', views.viajesAceptaRechaza, name="viajes_acepta_rechaza"),

   ### METODO POST ACTUALIZA ESTADO POSICION
   path('data-actualiza-posicion', views.actualizaEstadoPosicion, name="actualiza_estado_posicion"),

   ### METODO DATA MUESTRA DATOS DE ACPTADOS
   path('data-viajes-aceptado/chofer=<str:chofer>', views.datosViajesAceptados, name="datos_viajes_aceptados"),

   ### METODO POST ACTUALIZA ESTADO DEL CHOFER
   path('data-actualiza-estado/chofer', views.actualizaEstadoChofer, name="actualiza_estado_chofer"),

   ### METODO DATA FINALIZA REMITO 
   path('data-finaliza-remito/idAsignacion=<str:idAsignacion>', views.finalizaRemito, name="finaliza_remito"),

   ### GUARDA COSECHA DIARIA
   path('data-inserta/cosecha-diaria', views.guardaCosechaDiaria, name="cosecha_diaria"),

   ### MUESTRA LA COSECHA POR FECHA
   path('data-ver/cosecha-diaria', views.verReporteBins, name="ver_cosecha_diaria"),


   ###################### PARTE NUEVA ###########################

   path('data-inicial-nuevo', views.Carga_Inicial_Flete, name="carga_inicial_flete"),

   #### MUESTRA CONTROL DE CALIDAD ENTRE FECHAS
   path('data-ver/cosecha-calidad', views.verReporteCalidad, name="ver_reporte_calidad"),

   #######################    ORIGENES Y DESTINOS DE PEDIDOS VARIOS ##############################
   path('data-ver/origen-destino/', views.Data_Destinos_Origenes, name="Data_Destinos_Origenes"),

]