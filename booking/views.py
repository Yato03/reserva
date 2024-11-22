from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Reserva
from django.http import HttpResponseForbidden
from usuario.models import Usuario, Notificacion
from usuario.views import es_sereno, es_usuario

# Create your views here.

@login_required
@user_passes_test(es_sereno, login_url='home')
def reservas_activas(request):
    # Obtener las reservas POR_CONFIRMAR y CONFIRMADA y ordenadas de forma descendente
    reservas = Reserva.objects.filter(estado__in=['POR_CONFIRMAR', 'CONFIRMADA']).order_by('-fecha_inicio')

    return render(request, 'reservas_activas.html', {'reservas': reservas})

@user_passes_test(es_usuario, login_url='reservas_activas')
@login_required
def mis_reservas(request):
    # Obtener las reservas del usuario logueado 
    usuario = Usuario.objects.get(user=request.user)
    reservas = request.user.reservas.all()
    return render(request, 'mis_reservas.html', {'reservas': reservas})

@login_required
def cancelar_reserva(request, reserva_id):
    # Obtener la reserva a cancelar
    reserva = Reserva.objects.get(id=reserva_id)
    if reserva.usuario != request.user and not es_sereno(request.user):
        return HttpResponseForbidden()
    # Cancelar la reserva
    reserva.estado = 'CANCELADA'
    reserva.save()

    # Crear notificacion

    crear_notificacion(reserva, "cancelada")

    return redirect('mis_reservas')

def finalizar_reserva(request, reserva_id):
    # Obtener la reserva a finalizar
    reserva = Reserva.objects.get(id=reserva_id)
    if not es_sereno(request.user):
        return HttpResponseForbidden()
    # Finalizar la reserva
    reserva.estado = 'FINALIZADA'
    reserva.save()

    # Crear notificacion
    crear_notificacion(reserva, "finalizada")

    return redirect('reservas_activas')

def confirmar_reserva(request, reserva_id):
    # Obtener la reserva a confirmar
    reserva = Reserva.objects.get(id=reserva_id)
    if not es_sereno(request.user):
        return HttpResponseForbidden()
    # Confirmar la reserva
    reserva.estado = 'CONFIRMADA'
    reserva.save()

    # Crear notificacion
    crear_notificacion(reserva, "confirmada")

    return redirect('reservas_activas')


def crear_notificacion(reserva, tipo):
    dia = reserva.fecha_inicio.day
    mes = reserva.fecha_inicio.month
    anio = reserva.fecha_inicio.year
    hora = reserva.fecha_inicio.hour

    usuario = Usuario.objects.get(user=reserva.usuario)

    Notificacion.objects.create(
        usuario=usuario,
        titulo=f"Reserva {tipo}",
        mensaje=f"La reserva del espacio comun {reserva.espacio_comun.nombre} para el día {dia}/{mes}/{anio} a las {hora}:00 ha sido {tipo}.",
    )