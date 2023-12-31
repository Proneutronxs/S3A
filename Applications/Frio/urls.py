from django.urls import path
from Applications.Frio import views

urlpatterns = [
    
    path('', views.Frio, name="frio"),

    path('horas-extras/', views.HorasExtrasFrio, name='horas_extras_frio'),

    path('horas-extras/autoriza', views.AutorizaHorasExtrasFrio, name='horas_extras_frio_autoriza'),

    path('horas-extras/autoriza/carga-combox-cc', views.cargaCentrosCostosFrio, name='horas_extras_cc_frio'),

    path('horas-extras/autoriza/ver-horas-extras', views.mostrarHorasCargadasPorCCFrio, name='horas_extras_cc_frio'),

    path('horas-extras/autoriza/elimina/horas-extras', views.eliminaHorasSeleccionadasFrio, name='elimina_horas_extras_frio'),

    path('horas-extras/autoriza/horas-extras', views.autorizaHorasCargadas, name='elimina_horas_extras_frio'),
]