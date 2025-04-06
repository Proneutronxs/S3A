from django.urls import path
from Applications.Mobile.HorasExtras import views

urlpatterns = [

    ### CARGA Y MUESTRA LOS MOTIVOS PARA SELECCIONAR EL MOTIVO PARA LAS HORAS EXTRAS
    path('mostrar/motivos/horasextras', views.motrar_MotivosHE, name="mostrar_MotivosHorasExtras"),

    ### INSERTA LAS HORAS EXTRAS ENVÍADAS HORAS EXTRAS A AUTORIZAR (POST BODY REQUEST)
    path('inserta/horas_extras', views.insert_HoraExtra, name="inserta_horasExtras"),

    ### MUESTRA HORAS EXTRAS ACTIVAS - PETICIONES DE HORAS EXTRAS (GET BODY REQUEST) ----------------------------------------NO SE USAN
    path('mostrar/horasextras/activas', views.mostrarHoraExtrasActivas, name="muestra_horasExtras_activas"),

    ### GUARDA LAS HORAS EXTRAS EN S3A UBICACIÓN Y CONCATENACIÓN CON EL ID (ACTUALIZA EL ESTADO DE LA PETICIÓN)--------------NO SE USA
    path('inserta/horasextras/s3a', views.enviarHorasExtras, name="envia_horasExtras_s3a."),

    ####MUESTRA LAS FECHAS QUE SE CARGARONHORAS EXTRAS
    path('muestra/fechas-he/mes=<str:mes>&user=<str:usuario>', views.verCargaFechasDeHorasExtras, name="ver_Carga_fechas_horas_extras"),

    ### MUESTAR POR LA FECHA ENVÍADA LAS HORAS EXTRAS CARGADAS
    path('muestra/horas-extras-cargadas', views.verHorasExtras, name="ver_horas_extras"),



    ##### NUEVO
    path('lista-legajos/', views.busca_legajos_horas_extras, name="busca_legajos_horas_extras"),
    
    path('lista-horas/', views.busca_horas_extras_legajo, name="busca_horas_extras_legajo"),
]