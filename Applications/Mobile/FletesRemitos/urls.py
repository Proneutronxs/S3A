from django.urls import path
from Applications.Mobile.FletesRemitos import views

urlpatterns = [
   
   ### DATA INICIAL PARA PEDIDO DE FLETES
   path('data-inicial', views.datos_Iniciales_Flete, name="data_inicial"),

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

   ### DATA BINS MARCA Y TIPO PARA REMITOS
   path('data-remitos/bins', views.obtieneMarcaBins, name="trae_idMarcas"),






]