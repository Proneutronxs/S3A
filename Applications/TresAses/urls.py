from django.urls import path
from Applications.TresAses import views

urlpatterns = [

    ### SOLO RENDERIZADO
    path('', views.TresAses, name="tresases"),
    path('verificar/permisos&sector=<str:sector>', views.verificarPermisos, name="verificarPermisos"),

]