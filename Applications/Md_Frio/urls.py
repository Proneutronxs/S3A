from django.urls import path
from Applications.Md_Frio import views

urlpatterns = [

    ### CHACRAS MODULO HORAS EXTRAS
    path('', views.Md_Frio, name="Md_Frio_index"),

    path('autoriza-horas/', views.Autoriza_Horas_Extras, name="Md_Frio_Autoriza_Horas_Extras"),

    path('autoriza-horas/data-inicial/', views.Centros_por_Usuario, name="Md_Frio_Centros_por_Usuario"),

    path('autoriza-horas/personal-horas/', views.combox_lista_personal_horas_extras, name="Md_Frio_combox_lista_personal_horas_extras"),

    path('autoriza-horas/listado-data/', views.data_listado_horas_extras, name="Md_Frio_data_listado_horas_extras"),

    

]