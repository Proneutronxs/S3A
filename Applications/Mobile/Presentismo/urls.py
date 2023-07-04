from django.urls import path
from Applications.Mobile.Presentismo import views

urlpatterns = [

### PRUEBA DATA
path('data/', views.data, name="data"),

### INSERT DE FICHADAS MASIVAS (MANDA UN BODY REQUEST)
path('inserta/fichadas', views.insert_fichada, name="inserta_fichadas"),

]