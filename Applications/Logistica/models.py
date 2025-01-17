from django.db import models

# Create your models here.

class Logistica(models.Model):
    class Meta:
        permissions = [
            ("puede_ingresar", "Puede Ingresar"),
            ("puede_ver", "Puede Ver"),
            ("puede_insertar", "Puede Insertar"),
            ("puede_modificar", "Puede Modificar"),
            ("puede_borrar", "Puede Borrar"),
            ("puede_autorizar", "Puede Autorizar HE"),
            ("puede_denegar", "Puede Denegar HE"),
            ("puede_restaurar", "Puede Restaurar HE"),
            ("puede_dar_baja", "Puede Dar de Baja PF"),
        ]
