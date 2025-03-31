from django.urls import path
from Applications.Md_Rrhh import views

urlpatterns = [

    ### CHACRAS MODULO HORAS EXTRAS
    path('', views.Md_Rrhh, name="Md_Rrhh_index"),





    

    path('archivo-isis/', views.Archivo_Isis, name="Md_Rrhh_Archivo_Isis"),

    path('archivo-isis/listar-data/', views.data_listado_horas_extras_isis, name="Md_Rrhh_data_listado_horas_extras_isis"),

    path('archivo-isis/archivo=<str:filename>', views.descarga_archivo_excel, name="Md_Chacras_descarga_archivo_excel"),

    # path('mobile/horas-extras/enviar-horas/', views.inserta_elimina_horas_extras, name="Md_Chacras_inserta_elimina_horas_extras"),

    

]