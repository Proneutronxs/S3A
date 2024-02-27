from django.urls import path
from Applications.Bascula import views

urlpatterns = [

    ### REDIRECCIÓN A EMPAQUE
    path('', views.Bascula, name="bascula"),

    path('remitos/', views.remitos, name='_remitos'),

    path('remitos-chacras/', views.verRemitosChacras, name='ver_remitos_chacras'),

    path('remitos-chacras/listado-remitos/', views.listadoRemitos, name='listado_remitos'),

    path('remitos-chacras/busca-remito/', views.buscaRemito, name='busca_remito'),

    path('remitos-chacras/verifica-modifica/', views.verificaModificaRemito, name='verifica_modifica_remito'),

    path('remitos-chacras/verifica-crea-nuevo/', views.verificaCreaNuevoRemito, name='verifica_nuevo_remito'),

    path('remitos-chacras/actualiza-obs/', views.actualizaObsRemito, name='actualiza_obserbaciones'),

    path('remitos-chacras/descarga-pdf/', views.donwloadPdf, name='crea_descarga'),

    path('remitos-chacras/carga-especie-marca/', views.llamaEspecieMarca, name='especie_chacra'),

    path('remitos-chacras/carga-envase/', views.traeTipoEnvase, name='carga_envase'),

    path('remitos-chacras/actualiza-datos/', views.actualizaDatos, name='actualiza_datos'),

    path('remitos-chacras/modifica-up/', views.actualizaUP, name='actualiza_up'),

    path('remitos-chacras/elimina-remito/', views.eliminaRemito, name='elimina-remito'),

    path('remitos-chacras/listado-variedades/', views.llama_variedades, name='llama_variedades'),

    path('remitos-chacras/modifica-variedad/', views.actualizaVariedad, name='actualiza_variedad'),

]