from django.urls import path
from Applications.Bascula import views

urlpatterns = [

    ### REDIRECCIÓN A EMPAQUE
    path('', views.Bascula, name="bascula"),

    path('remitos/', views.remitos, name='_remitos'),

    path('remitos-chacras/', views.verRemitosChacras, name='ver_remitos_chacras'),

    path('remitos-chacras/listado-remitos/', views.listadoRemitos, name='listado_remitos'),

    path('remitos-chacras/busca-remito/', views.buscaRemito, name='busca_remito'),

    path('remitos-chacras/modifica/', views.verificaModificaRemito, name='verifica_modifica_remito'),

    path('remitos-chacras/actualiza-obs/', views.actualizaObsRemito, name='actualiza_obserbaciones'),


]