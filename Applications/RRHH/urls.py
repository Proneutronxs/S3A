from django.urls import path
from Applications.RRHH import views

urlpatterns = [

    ### REDIRECCIÓN A RRHH
    path('', views.RRHH, name="rrhh"),

    ### REDIRECCIÓN A HORAS EXTRAS
    path('horas-extras/', views.horasExtras, name="horasExtras"),

    path('horarios/', views.Horarios, name="Horarios"),

    path('horarios/agregar', views.agregarHorarios, name="agrega_horarios"),

    ### REDIRECCIÓN A HORAS EXTRAS
    path('horas-extras/transferencia', views.transferenciaHorasExtras, name="horasExtrasTrasnferir"),

    ### URL MOSTRAR HORAS EXTRAS
    path('horas-extras/transferencia/ver/listado-horas', views.mostrarHorasCargadas, name="verHorasExtrasTransferir"),

    ###MUESTRA TODAS LAS HORAS PETICIÖN GET
    path('horas-extras/transferencia/ver/listado-horas-todo', views.traeTodo, name="traeTodoHE"),

    ### URL MOSTRAR HORAS EXTRAS POR LEGAJOS
    path('horas-extras/transferencia/ver/listado-horas-legajos', views.mostrarHorasCargadasPorLegajo, name="verHorasExtrasTransferirLegajos"),

    ### URL ENVIAR HORAS EXTRAS
    path('horas-extras/transferencia/enviar/listado-horas', views.enviarHorasCargadas, name="enviarHorasExtrasTransferir"),

    ### URL CARGA COMBOX POR LEGAJO
    path('horas-extras/transferencia/cargar-combox-legajos', views.cargaLegajos, name="cargaComboxLegajos"),

    ### URL ELIMINAHORAS EXTRAS
    path('horas-extras/transferencia/elimina/listado-horas', views.eliminaHorasCargadas, name="eliminaHorasCargadas"),



    #### ARCHIVOS A EXPORTAR ####

    path('archivos/', views.Archivos, name="archivos"),

    path('archivos/ver/listado-horas/', views.mostrarHorasArchivo, name="archivos_mostrar_horas"),

    path('archivos/descarga-excel-he/', views.CreaExcelISIS, name="archivos_excel_horas"),


    #### RANKING DE FALTAS ####

    path('ranking/', views.Ranking, name="ranking"),

    path('ranking/ranking-faltas', views.RankingFaltas, name="ranking_faltas"),

]