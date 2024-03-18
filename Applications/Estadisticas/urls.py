from django.urls import path
from Applications.Estadisticas import views

urlpatterns = [

    ### REDIRECCIÓN A EMPAQUE
    path('', views.Estadisticas, name="estadisticas"),

    path('cosecha/', views.Cosecha, name="cosecha"),

    path('cosecha/ver-estadisticas/', views.estadisticaCosecha, name="cosecha_estadisticas"),

    

]