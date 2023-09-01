from django.urls import path
from Applications.Empaque import views

urlpatterns = [

    ### REDIRECCIÓN A EMPAQUE
    path('', views.Empaque, name="empaque"),

    path('horas-extras/', views.HorasExtrasEmpaque, name='horas_extras_empaque'),

    path('horas-extras/autoriza', views.AutorizaHorasExtrasEmpaque, name='horas_extras_empaque_autoriza'),

    path('horas-extras/autoriza/carga-combox-legajos', views.cargaLegajosEmpaque, name='horas_extras_legajos_empaque'),

    path('horas-extras/autoriza/ver-horas-legajos', views.mostrarHorasCargadasPorLegajoEmpaque, name='ver_horas_extras_legajos_empaque'),
    
    path('horas-extras/autoriza/enviar/estado-horas-legajos', views.autorizaHorasCargadas, name='autoriza_horas_extras_seleccionadas'),

    path('horas-extras/autoriza/elimina/estado-horas-legajos', views.eliminaHorasSeleccionadas, name='elimina_horas_extras_seleccionadas'),

]