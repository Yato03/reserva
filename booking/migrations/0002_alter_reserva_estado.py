# Generated by Django 3.2.25 on 2024-11-20 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reserva',
            name='estado',
            field=models.CharField(choices=[('POR_CONFIRMAR', 'Por Confirmar'), ('CONFIRMADA', 'Confirmada'), ('FINALIZADA', 'Finalizada'), ('CANCELADA', 'Cancelada')], default='POR_CONFIRMAR', max_length=15, verbose_name='Estado'),
        ),
    ]
