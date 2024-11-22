from django.shortcuts import render, redirect
from usuario.views import es_sereno
# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if es_sereno(request.user):
            return redirect('reservas_activas')
        else:
            return redirect('listar_espacios_comunes')
    return render(request, 'home.html')
