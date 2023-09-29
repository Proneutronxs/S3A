from django.db import models

# Create your models here.


class CapturaErroresSQL(models.Model):
    Aplicacion = models.CharField(max_length=45)
    Funcion = models.CharField(max_length=45)
    Usuario = models.CharField(max_length=45)
    Error= models.TextField()
    Fecha = models.DateTimeField()

class CapturaContraseñas(models.Model):
    Usuario = models.CharField(max_length=45)
    ContraseñaVieja = models.CharField(max_length=45)
    ContraseñaNueva = models.CharField(max_length=45)
    Fecha = models.DateTimeField()

class CapturaRegistros(models.Model):
    Aplicacion = models.CharField(max_length=45)
    Funcion = models.CharField(max_length=45)
    Usuario = models.CharField(max_length=45)
    Accion = models.CharField(max_length=45, null=True)
    Realiza = models.CharField(max_length=45)
    Fecha = models.DateTimeField()  