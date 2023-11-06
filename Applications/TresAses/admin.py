from django.contrib import admin
from Applications.TresAses.models import *
from Applications.Inicio.models import *

# Register your models here.
admin.site.register(CapturaContraseñas)
admin.site.register(UserProfile)
admin.site.register(CapturaErroresSQL)
admin.site.register(CapturaRegistros)