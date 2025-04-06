from django.urls import path
from Applications.Md_Frio import views

urlpatterns = [

    ### CHACRAS MODULO HORAS EXTRAS
    path('', views.Md_Frio, name="Md_Frio_index"),



    path('horas-extras/autoriza/', views.Autoriza_Horas_Extras, name="Md_Frio_Autoriza_Horas_Extras"),

    path('horas-extras/autoriza/data-inicial/', views.Centros_por_Usuario, name="Md_Frio_Centros_por_Usuario"),

    path('horas-extras/autoriza/personal-centro/', views.combox_lista_personal_centro, name="Md_Frio_combox_lista_personal_centro"),

    path('horas-extras/autoriza/listado-data/', views.data_listado_horas_extras, name="Md_Frio_data_listado_horas_extras"),

    path('horas-extras/autoriza/enviar-horas/', views.inserta_elimina_horas_extras, name="Md_Frio_inserta_elimina_horas_extras"),



    path('horas-extras/listado/', views.Listado_Horas_Extras, name="Md_Frio_Listado_Horas_Extras"),

    path('horas-extras/listado/data-inicial/', views.Centros_por_Usuario, name="Md_Frio_Centros_por_Usuario_listado"),

    path('horas-extras/listado/personal-centro/', views.combox_lista_personal_centro, name="Md_Frio_combox_lista_personal_centro_listado"),

    path('horas-extras/listado/archivo=<str:filename>', views.descarga_archivo_excel, name="Md_Frio_descarga_archivo_excel"),

    path('horas-extras/listado/reporte-web/', views.data_listado_horas_extras_web, name="Md_Frio_data_listado_horas_extras_web"),





    

]