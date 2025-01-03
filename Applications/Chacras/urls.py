from django.urls import path
from Applications.Chacras import views
from S3A.funcionesGenerales import *
urlpatterns = [

    path('', views.Chacras, name="chacras"),

    path('planillas/', views.planillas, name='_planillas'),

    path('planillas/general/', views.general, name='planilla_general'),

    path('planillas/general/listar-centros/', views.listaAbrevCentros, name='planilla_general_lista_centros'),

    path('planillas/general/listar-personal/', views.listaPersonalPorCentro, name='planilla_general_lista_personal_centro'),

    path('planillas/general/listar-adicionales/', views.listarAdicionales, name='planilla_general_listar_adicionales'),

    path('planillas/general/eliminar-adicionales/', views.eliminaAdicionalTildado, name='planilla_general_eliminar_adicionales'),

    path('planillas/general/inserta-premio-adicionales/', views.insertaPremioAdicional, name='planilla_general_inserta_premio_adicionales'),

    path('planillas/general/inserta-importe-adicionales/', views.insertaImporteAdicional, name='planilla_general_inserta_importe_adicionales'),

    path('planillas/general/detalle-adicional/', views.detalleAdicional, name='planilla_general_detalle_adicional'),

    path('planillas/general/crear-archivos/', views.crearArchivos, name='planilla_general_crear_archivos'),
    
]