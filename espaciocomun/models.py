from django.db import models

# Create your models here.

class EspacioComun(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    capacidad = models.IntegerField()
    direccion = models.TextField()
    def __str__(self):
        return self.nombre