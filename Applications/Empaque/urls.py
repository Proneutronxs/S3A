from django.urls import path
from Applications.Empaque import views

urlpatterns = [

    ### REDIRECCIÓN A EMPAQUE
    path('', views.Empaque, name="empaque"),

    path('horas-extras/', views.HorasExtrasEmpaque, name='horas_extras_empaque'),

    path('horas-extras/autoriza', views.AutorizaHorasExtrasEmpaque, name='horas_extras_empaque_autoriza'),

    path('horas-extras/agrega', views.AgregaAutorizadosEmpaque, name='agrega_autorizados_empaque'),

    path('horas-extras/agrega/lista-personal', views.personal_por_Ccostos, name='personal_por_Ccostos'),

    path('horas-extras/agrega/guarda-personal', views.guardaPersonalTildado, name='guarda_personal'),

    path('horas-extras/agrega/muestra-personal', views.muestraPersonalAutorizado, name='muestra_personal_autorizado'),

    path('horas-extras/agrega/elimina-personal', views.eliminaPersonalTildado, name='elimina_personal'),

    path('horas-extras/autoriza/carga-combox-legajos', views.cargaLegajosEmpaque, name='horas_extras_legajos_empaque'),

    path('horas-extras/autoriza/ver-horas-legajos', views.mostrarHorasCargadasPorLegajoEmpaque, name='ver_horas_extras_legajos_empaque'),
    
    path('horas-extras/autoriza/enviar/estado-horas-legajos', views.autorizaHorasCargadas, name='autoriza_horas_extras_seleccionadas'),

    path('horas-extras/autoriza/elimina/estado-horas-legajos', views.eliminaHorasSeleccionadas, name='elimina_horas_extras_seleccionadas'),

    ###### HORAS PROCESADAS ###### NUEVO MODULO

    path('horas-extras/envia', views.EnviaHorasProcesadasEmpaque, name='horas_extras_autoriza_nuevo'),

    path('horas-extras/envia/lista-procesadas', views.listaHorasProcesadas, name='lista_horas_procesadas'),

    path('horas-extras/envia/tranferir-personal', views.transfierePersonalTildado, name='tranfiere_personal_tildado'),

    path('horas-extras/envia/elimina-personal', views.eliminaPersonalProcesado, name='envia_elimina_personal_procesado'),
]