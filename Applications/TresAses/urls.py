from django.urls import path
from Applications.TresAses import views

urlpatterns = [

    ### SOLO RENDERIZADO
    path('', views.TresAses, name="tresases"),



]