from django.urls import path
from Applications.Mobile.Anticipos import views

urlpatterns = [
    ### INSERT DE FICHADAS MASIVAS (MANDA UN BODY REQUEST)
    path('inserta/anticipo', views.insert_anticipos, name="inserta_anticipos"),
    #### BODY DE BUSCAR ANTICPOS
    path('muestra/anticipo', views.verAnticipos, name="ver_anticipos"),
    ### GET BUSCA FECHAS
    path('muestra/fechas-anticipo/<str:mes>/str:usuario>', views.cargaFechasDeAnticipos, name="cargaFechasDeAnticipos"),
]