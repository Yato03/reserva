# Generated by Django 3.2.25 on 2024-11-23 17:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_notificacion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(blank=True, max_length=15, null=True, validators=[django.core.validators.RegexValidator('^\\d+$', 'El teléfono debe contener solo dígitos.'), django.core.validators.MinLengthValidator(8, 'El teléfono debe tener al menos 8 dígitos.'), django.core.validators.MaxLengthValidator(15, 'El teléfono no debe exceder los 15 dígitos.')], verbose_name='Número de Teléfono'),
        ),
    ]
