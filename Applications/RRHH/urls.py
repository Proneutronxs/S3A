from django.urls import path
from Applications.RRHH import views

urlpatterns = [

    ### REDIRECCIÓN A RRHH
    path('', views.RRHH, name="rrhh"),

    ### REDIRECCIÓN A HORAS EXTRAS
    path('horas-extras/', views.horasExtras, name="horasExtras"),

    ### REDIRECCIÓN A HORAS EXTRAS
    path('horas-extras/transferencia', views.transferenciaHorasExtras, name="horasExtrasTrasnferir"),

    ### URL MOSTRAR HORAS EXTRAS
    path('horas-extras/transferencia/ver/listado-horas', views.mostrarHorasCargadas, name="verHorasExtrasTransferir"),

    ### URL MOSTRAR HORAS EXTRAS POR LEGAJOS
    path('horas-extras/transferencia/ver/listado-horas-legajos', views.mostrarHorasCargadasPorLegajo, name="verHorasExtrasTransferirLegajos"),

    ### URL ENVIAR HORAS EXTRAS
    path('horas-extras/transferencia/enviar/listado-horas', views.enviarHorasCargadas, name="enviarHorasExtrasTransferir"),

    ### URL CARGA COMBOX POR LEGAJO
    path('horas-extras/transferencia/cargar-combox-legajos', views.cargaLegajos, name="cargaComboxLegajos"),
    ### URL ELIMINAHORAS EXTRAS
    path('horas-extras/transferencia/elimina/listado-horas', views.eliminaHorasCargadas, name="eliminaHorasCargadas"),

]