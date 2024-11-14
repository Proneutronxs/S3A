from django.urls import path
from Applications.TresAses import views

urlpatterns = [

    ### SOLO RENDERIZADO
    path('', views.TresAses, name="tresases"),
    path('verificar/permisos&sector=<str:sector>', views.verificarPermisos, name="verificarPermisos"),




    path('prueba-subir-archivos/', views.push, name="noti_push"),

    path('prueba-subir-archivos/sube-archivo/', views.recibir_archivos, name="recibir_archivos"),

] 