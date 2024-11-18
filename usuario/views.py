from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Usuario

# Create your views here.
def registrar_usuario(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirigir a la página de inicio de sesión
    else:
        form = RegisterForm()
    return render(request, 'registro.html', {'form': form})

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