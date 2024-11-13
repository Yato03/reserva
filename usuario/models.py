from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator

# Create your models here.

class Usuario(models.Model):
    class RolChoices(models.TextChoices):
        SERENO = 'SERENO', 'Sereno'
        USUARIO = 'USUARIO', 'Usuario'
        ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dni = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(r'^\d{8}$', 'El DNI debe contener exactamente 8 dígitos.')
        ],
        verbose_name="DNI"
    )
    rol = models.CharField(
        max_length=15,
        choices=RolChoices.choices,
        default=RolChoices.USUARIO,
        verbose_name="Rol"
    )
    telefono = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(r'^\d+$', 'El teléfono debe contener solo dígitos.'),
            MinLengthValidator(8, 'El teléfono debe tener al menos 8 dígitos.'),
            MaxLengthValidator(15, 'El teléfono no debe exceder los 15 dígitos.')
        ],
        verbose_name="Número de Teléfono"
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_rol_display()}"
