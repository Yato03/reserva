from django.db import models

# Create your models here.

class EspacioComun(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()
    capacidad = models.IntegerField()
    direccion = models.TextField()
    def __str__(self):
        return self.nombre

class EspacioComunImagen(models.Model):
    espacio_comun = models.ForeignKey(
        EspacioComun,
        on_delete=models.CASCADE,
        related_name='imagenes',
        verbose_name='Espacio Común'
    )
    url = models.URLField(max_length=200, verbose_name="URL de la Imagen")
    texto_alternativo = models.CharField(
        max_length=255, 
        verbose_name="Texto Alternativo",
        help_text="Texto que describe la imagen para accesibilidad"
    )

    def __str__(self):
        return f"Imagen de {self.espacio_comun.nombre}: {self.texto_alternativo[:50]}"