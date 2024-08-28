from django.urls import path
from Applications.Chacras import views
from S3A.funcionesGenerales import *
urlpatterns = [

    path('', views.Chacras, name="chacras"),

    path('planillas/', views.planillas, name='_planillas'),

    path('planillas/general/', views.general, name='planilla_general'),

    path('planillas/general/listar-centros/', views.listaCentros, name='planilla_general_lista_centros'),

    path('planillas/general/listar-personal/', views.listaPersonalPorCentro, name='planilla_general_lista_personal_centro'),

    path('planillas/general/listar-adicionales/', views.listarAdicionales, name='planilla_general_listar_adicionales'),
    
]