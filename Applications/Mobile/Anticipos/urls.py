from django.urls import path
from Applications.Mobile.Anticipos import views

urlpatterns = [
    ### INSERT DE FICHADAS MASIVAS (MANDA UN BODY REQUEST)
    path('inserta/anticipo', views.insert_anticipos, name="inserta_anticipos"),
]