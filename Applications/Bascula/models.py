from django.db import models

# Create your models here.
class Bascula(models.Model):
    class Meta:
        permissions = [
            ("puede_ingresar", "Puede Ingresar"),
            ("puede_ver", "Puede Ver"),
            ("puede_insertar", "Puede Insertar"),
            ("puede_modificar", "Puede Modificar"),
            ("puede_borrar", "Puede Borrar"),
            ("puede_crear_remito", "Puede Crear Remito"),
        ]