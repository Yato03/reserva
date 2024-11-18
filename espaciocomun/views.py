from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from .models import EspacioComun
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def listar_espacios_comunes(request):
    """
    Vista para listar todos los espacios comunes.
    """
    espacios = EspacioComun.objects.all()
    return render(request, 'listar_espacios_comunes.html', {'espacios': espacios})

@login_required
def detalle_espacio_comun(request, pk):
    """
    Vista para mostrar el detalle de un espacio común.
    """
    espacio = get_object_or_404(EspacioComun, pk=pk)
    imagenes = espacio.imagenes.all()  # Accede a las imágenes relacionadas
    return render(request, 'detalle_espacio_comun.html', {'espacio': espacio, 'imagenes': imagenes})
