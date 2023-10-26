from django.urls import path
from Applications.Mobile.FletesRemitos import views

urlpatterns = [
   
   ### DATA INICIAL PARA PEDIDO DE FLETES
   path('data-inicial', views.datos_Iniciales_Flete, name="data_inicial"),

   ### DATA SEGUN ID DE PRODUCTOR
   path('data-productor/idProductor=<str:idProductor>', views.idProductor_Chacra_Zona, name="idPrductor_Chacra_Zona"),

   ### DATA SEGUN ID DE ESPECIE
   path('data-especie/idEspecie=<str:idEspecie>', views.idEspecie_Varierad, name="idEspecie_Variedad"),



]