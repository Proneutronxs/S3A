from django.urls import path
from Applications.Chacras import views

urlpatterns = [

    path('', views.Chacras, name="chacras"),

    path('planillas/', views.planillas, name='_planillas'),

    path('planillas/general/', views.general, name='planilla_general'),
    
]