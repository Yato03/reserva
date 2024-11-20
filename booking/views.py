from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Reserva
from django.http import HttpResponseForbidden

# Create your views here.

@login_required
def mis_reservas(request):
    # Obtener las reservas del usuario logueado 
    reservas = request.user.reservas.all()
    return render(request, 'mis_reservas.html', {'reservas': reservas})

def cancelar_reserva(request, reserva_id):
    # Obtener la reserva a cancelar
    reserva = Reserva.objects.get(id=reserva_id)
    if reserva.usuario != request.user:
        return HttpResponseForbidden()
    # Cancelar la reserva
    reserva.estado = 'CANCELADA'
    reserva.save()
    return redirect('mis_reservas')