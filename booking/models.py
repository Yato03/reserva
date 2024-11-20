from django.db import models
from django.contrib.auth.models import User
from espaciocomun.models import EspacioComun  # Asegúrate de importar el modelo EspacioComun

class Reserva(models.Model):
    class EstadoChoices(models.TextChoices):
        PENDIENTE = 'POR_CONFIRMAR', 'Por Confirmar'
        CONFIRMADA = 'CONFIRMADA', 'Confirmada'
        FINALIZADA = 'FINALIZADA', 'Finalizada'
        CANCELADA = 'CANCELADA', 'Cancelada'

    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name="Usuario"
    )
    espacio_comun = models.ForeignKey(
        EspacioComun,
        on_delete=models.CASCADE,
        related_name='reservas',
        verbose_name="Espacio Común"
    )
    fecha_inicio = models.DateTimeField(verbose_name="Fecha de Inicio")
    fecha_fin = models.DateTimeField(verbose_name="Fecha de Fin")
    estado = models.CharField(
        max_length=15,
        choices=EstadoChoices.choices,
        default=EstadoChoices.PENDIENTE,
        verbose_name="Estado"
    )

    def __str__(self):
        return f"Reserva de {self.usuario.username} en {self.espacio_comun.nombre} ({self.fecha_inicio} - {self.fecha_fin})"
