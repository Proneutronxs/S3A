from django.urls import path
from Applications.Mobile.GeneralApp import views

urlpatterns = [

### sólo renderizado
path('subir-aplicacion/', views.subirApp, name="subirApp"),
path('subir-aplicacion/recibir_apk/', views.recibir_apk, name='recibir_apk'),
path('descargar-app/<str:nombre_apk>', views.descargar_apk, name='descargar_apk'),
### LOGIN DE LA APLICACION
path('login_App', views.login_app, name="login_App"),

### ID Y CHACRAS DEL USUARIO LOGUEADO (Parametro ID de USER Logueado)
path('codigo/centro_costos/id=<int:legajo>', views.id_Nombre_Ccostos, name="id_detalle_Ccostos"),

### PERSONAL POR CENTROS DE COSTOS (parametro Cod: de Centro de Costos)
path('personal/centro_costos/asistencia/id=<int:codigo>', views.personal_por_Ccostos_asistencia, name="personal_por_Ccostos_asistencia"),

path('personal/centro_costos/anticipos/id=<int:codigo>', views.personal_por_Ccostos_anticipos, name="personal_por_Ccostos_anticipos"),


]