from django.urls import path
from Applications.Api import views
from S3A.funcionesGenerales import *
urlpatterns = [

    path('data-general/', views.dataGeneral, name="data-general-api"),
    
]