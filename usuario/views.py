from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Usuario, Notificacion
import re

# Create your views here.

def es_sereno(user):
    usuario = Usuario.objects.get(user=user)
    return usuario.rol == 'SERENO' or usuario.rol == 'ADMINISTRADOR'

def es_usuario(user):
    usuario = Usuario.objects.get(user=user)
    return usuario.rol == 'USUARIO' or usuario.rol == 'ADMINISTRADOR'

def registrar_usuario(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirigir a la página de inicio de sesión
    else:
        form = RegisterForm()
    return render(request, 'registro.html', {'form': form})

@login_required
def editar_perfil(request):
    """
    Vista para editar el perfil del usuario autenticado.
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        usuario = None  # Maneja el caso en el que no exista un perfil asociado

    if request.method == 'POST':
        telefono = request.POST.get('telefono')
        usuario.telefono = telefono
        # Validar que el teléfono tenga 9 dígitos
        if not re.match(r'^\d{9}$', telefono):
            print("error")
            messages.error(request, "El teléfono debe tener 9 dígitos.")
        else:
            usuario.save()
            messages.success(request, "Perfil actualizado exitosamente.")
            return redirect('perfil')

    return redirect('perfil')

def login_view(request):
    """
    Vista para manejar el inicio de sesión de usuarios.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenido {user.username}!")
            return redirect('home')  # Cambia 'home' por el nombre de tu vista principal
        else:
            messages.error(request, "Nombre de usuario o contraseña incorrectos.")
    else:
        if request.user.is_authenticated:
            return redirect('home')

    return render(request, 'login.html')

@login_required
def perfil_usuario(request):
    """
    Vista para mostrar el perfil del usuario autenticado.
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
    except Usuario.DoesNotExist:
        usuario = None  # Maneja el caso en el que no exista un perfil asociado

    context = {
        'usuario': usuario,
    }
    return render(request, 'perfil_usuario.html', context)


def logout_view(request):
    """
    Vista para manejar el cierre de sesión de usuarios.
    """
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('login')

@login_required
def mis_notificaciones(request):
    """
    Vista para mostrar las notificaciones del usuario autenticado.
    """
    try:
        usuario = Usuario.objects.get(user=request.user)
        notificaciones = Notificacion.objects.filter(usuario=usuario)
    except Usuario.DoesNotExist:
        usuario = None  # Maneja el caso en el que no exista un perfil asociado
        notificaciones = None

    context = {
        'usuario': usuario,
        'notificaciones': notificaciones,
    }
    return render(request, 'mis_notificaciones.html', context)