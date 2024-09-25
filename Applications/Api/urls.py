from django.urls import path
from Applications.Api import views
from Applications.Api.vistas.CRC import demoCRC
from S3A.funcionesGenerales import *
urlpatterns = [

    path('data-general/', demoCRC.dataGeneral, name="data-general-api"),

    path('data-general/with-crc/', demoCRC.dataConCRC, name="data_general_api_con_crc"),
    




    
]