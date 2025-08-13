from django.urls import path
from Applications.Md_Rrhh import views

urlpatterns = [

    ### CHACRAS MODULO HORAS EXTRAS
    path('', views.Md_Rrhh, name="Md_Rrhh_index"),





    

    path('archivo-isis/', views.Archivo_Isis, name="Md_Rrhh_Archivo_Isis"),

    path('archivo-isis/data-inicial/', views.listaCentros, name="Md_Rrhh_listaCentros_isis"),

    path('archivo-isis/listar-data/', views.data_listado_horas_extras_isis, name="Md_Rrhh_data_listado_horas_extras_isis"),

    path('archivo-isis/sub-data/', views.data_legajos_x_centro, name="Md_Rrhh_data_legajos_x_centro_isis"),

    path('archivo-isis/archivo=<str:filename>', views.descarga_archivo_excel, name="Md_Chacras_descarga_archivo_excel"),

    # path('mobile/horas-extras/enviar-horas/', views.inserta_elimina_horas_extras, name="Md_Chacras_inserta_elimina_horas_extras"),

    path('chacras/listado-sipreta/', views.Listado_Sipreta, name="Md_Rrhh_Listado_Sipreta"),

    path('chacras/listado-sipreta/lista-centros-chacras/', views.listaCentrosChacras, name="Md_Rrhh_listaCentrosChacras"),

    path('chacras/listado-sipreta/listado-labores/', views.data_listado_planilla_labores, name="Md_Rrhh_data_listado_planilla_labores"),

    path('chacras/listado-sipreta/archivo=<str:filename>', views.descarga_archivo_excel, name="Md_Rrhh_descarga_archivo_excel"),



    path('chacras/reportes-labores-personal/', views.Listado_Labores, name="Md_Rrhh_Listado_Labores"),

    path('chacras/reportes-labores-personal/data-inicial/', views.carga_inicial_listado_labores, name="Md_Rrhh_carga_inicial_listado_labores"),

    path('chacras/reportes-labores-personal/chacra-productor/', views.listado_combox_chacras_x_productor, name="Md_Rrhh_listado_combox_chacras_x_productor_X"),

    path('chacras/reportes-labores-personal/chacra-personal-cuadros/', views.cuadro_personal_x_chacra, name="Md_Rrhh_uadro_personal_x_chacra_X"),
    
    path('chacras/reportes-labores-personal/detalle-labores/', views.listado_detalle_labores, name="Md_Rrhh_listado_detalle_labores"),
    
    path('chacras/reportes-labores-personal/descarga-archivo/', views.archivo_detalle_labores, name="Md_Rrhh_archivo_detalle_labores"),
    
    path('chacras/reportes-labores-personal/archivo=<str:filename>', views.descarga_archivo_excel, name="Md_Rrhh_descarga_archivo_excel"),

    

]