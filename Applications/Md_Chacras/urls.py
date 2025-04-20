from django.urls import path
from Applications.Md_Chacras import views

urlpatterns = [

    ### CHACRAS MODULO HORAS EXTRAS
    path('', views.Md_Chacras, name="Md_Chacras_index"),



    path('sipreta/presupuesto/', views.Presupuesto, name="Md_Chacras_Presupuesto"),

    path('sipreta/presupuesto/combox-productores/', views.listado_combox_productor, name="Md_Chacras_listado_combox_productor"),

    path('sipreta/presupuesto/combox-chacras/', views.listado_combox_chacras_x_productor, name="Md_Chacras_listado_combox_chacras_x_productor"),

    path('sipreta/presupuesto/data-listado/', views.listado_chacras_x_filas, name="Md_Chacras_listado_chacras_x_filas"),



    path('mobile/horas-extras/', views.Horas_Extras, name="Md_Chacras_Horas_Extras"),

    path('mobile/horas-extras/listar-horas-extras/', views.data_listado_horas_extras, name="Md_Chacras_data_listado_horas_extras"),

    path('mobile/horas-extras/archivo=<str:filename>', views.descarga_archivo_excel, name="Md_Chacras_descarga_archivo_excel"),

    path('mobile/horas-extras/enviar-horas/', views.inserta_elimina_horas_extras, name="Md_Chacras_inserta_elimina_horas_extras"),

    

]