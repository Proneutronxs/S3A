from django.urls import path
from Applications.Api import views
from Applications.Api.vistas.CRC import demoCRC
from Applications.Api.vistas.FruitTruck import fruit
from S3A.funcionesGenerales import *


urlpatterns = [

    path('data-general/', demoCRC.dataGeneral, name="data-general-api"),

    path('data-general/with-crc/', demoCRC.dataConCRC, name="data_general_api_con_crc"),
    


    ### CAMIONES APLICACION DE FRUIT TRUCK ###



    path('fruit/listar-transporte/', fruit.listarTransporte, name="choferes_listar_transportes"),

    path('fruit/listar-transporte/datos-transportes/', fruit.listarDataTransporte, name="choferes_listar_transportes_data_transportes"),

    path('fruit/listar-transporte/insertar-transporte/', fruit.guardar_transporte_chofer, name="guardar_transporte_chofer"),

]