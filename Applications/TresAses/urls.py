from django.urls import path
from Applications.TresAses import views

urlpatterns = [

    ### SOLO RENDERIZADO
    path('', views.TresAses, name="tresases"),
    path('verificar/permisos&sector=<str:sector>', views.verificarPermisos, name="verificarPermisos"),




    path('prueba-envia-notificaciones-push/', views.push, name="noti_push"),

    path('prueba-envia-notificaciones-push/envia/', views.notiPush, name="noti_push_envia"),

] 