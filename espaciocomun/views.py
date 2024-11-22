from django.shortcuts import render, get_object_or_404, redirect
from .models import EspacioComun
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime
import calendar
from booking.models import Reserva
from django.http import Http404
from usuario.models import Notificacion, Usuario
from booking.views import crear_notificacion
from usuario.views import es_usuario

# Create your views here.

@login_required
def listar_espacios_comunes(request):
    """
    Vista para listar todos los espacios comunes.
    """
    espacios = EspacioComun.objects.prefetch_related('imagenes')
    return render(request, 'listar_espacios_comunes.html', {'espacios': espacios})

@login_required
def detalle_espacio_comun(request, pk):
    """
    Vista para mostrar el detalle de un espacio común.
    """
    espacio = get_object_or_404(EspacioComun, pk=pk)
    imagenes = espacio.imagenes.all() 
    month = datetime.now().month
    year = datetime.now().year

    return render(request, 'detalle_espacio_comun.html', {'espacio': espacio, 'imagenes': imagenes, 'month': month, 'year': year, 'es_usuario': es_usuario(request.user)})


@login_required
@user_passes_test(es_usuario, login_url='reservas_activas')
def reserva_espacio_comun(request, pk, month, year):
    """
    Vista para reservar un espacio común.
    """

    espacio_comun = EspacioComun.objects.get(pk=pk)

    # Obtener los días con colores
    reservas = Reserva.objects.all()

    fechas_colores = dict()
    for reserva in reservas:
        if reserva.estado != 'CANCELADA' and reserva.espacio_comun == espacio_comun and reserva.estado != 'FINALIZADA':
            fechas_colores[reserva.fecha_inicio.date()] = 'naranja'

    # marcar en rojo los dias completos
    for fecha in fechas_colores:
        reservas_dia = [reserva for reserva in reservas if reserva.fecha_inicio.date() == fecha and reserva.estado != 'CANCELADA' and reserva.espacio_comun == espacio_comun and reserva.estado != 'FINALIZADA']
        horas_ocupadas = []
        for reserva in reservas_dia:
            horas_ocupadas.extend(generador_de_horas(reserva.fecha_inicio, reserva.fecha_fin))

        if len(horas_ocupadas) == 12:
            fechas_colores[fecha] = 'rojo'


    # Obtener el mes y año actual
    mes = month
    anio = year

    if anio < datetime.now().year or anio > datetime.now().year+1:
        anio = datetime.now().year

    if mes < 1 or mes > 12 or (anio == datetime.now().year and mes < datetime.now().month):
        mes = datetime.now().month

    # Generar el calendario del mes actual
    cal = calendar.Calendar()
    dias_mes = cal.itermonthdates(anio, mes)

    calendario_dias = [
        {
            'fecha': dia, 
            'color': fechas_colores.get(dia, 'blanco'),
            'weekday': dia.weekday()
        } 
        for dia in dias_mes
    ]

    return render(request, 'seleccion_reserva.html', {
        'calendario_dias': calendario_dias,
        'mes': mes,
        'anio': anio,
        'mes_anterior': mes - 1 if mes > 1 else 12,
        'anio_anterior': anio - 1 if mes == 1 else anio,
        'mes_siguiente': mes + 1 if mes < 12 else 1,
        'anio_siguiente': anio + 1 if mes == 12 else anio,
        'espacio': espacio_comun
    })

def generador_de_horas(fecha_inicio,fecha_final):
    """
    Genera un rango de horas entre dos fechas.
    """
    horas = []
    hora = fecha_inicio
    while hora < fecha_final:
        horas.append(hora.hour)
        hora = hora.replace(hour=hora.hour+1)
    return horas

@login_required
@user_passes_test(es_usuario, login_url='reservas_activas')
def reservar_dia(request, pk, month, year, day):
    """
    Vista para reservar un día.
    """
    # Obtener el día a reservar
    dia = day
    mes = month
    anio = year

    if anio < datetime.now().year or anio > datetime.now().year+1:
        anio = datetime.now().year

    if mes < 1 or mes > 12 or (anio == datetime.now().year and mes < datetime.now().month):
        mes = datetime.now().month

    if dia < 1 or dia > 31:
        dia = datetime.now().day

    # Obtener el espacio común
    espacio = EspacioComun.objects.get(pk=pk)

    # Obtener reservas de ese dia
    reservas = Reserva.objects.all()

    reservas = [reserva for reserva in reservas if reserva.fecha_inicio.date() == datetime(anio, mes, dia).date() and reserva.estado != 'CANCELADA' and reserva.espacio_comun == espacio and reserva.estado != 'FINALIZADA']

    horas_ocupadas = []
    
    for reserva in reservas:
        horas_ocupadas.extend(generador_de_horas(reserva.fecha_inicio, reserva.fecha_fin))

    horas_rango = [(hora, hora+1) for hora in range(9, 21)]

    fecha = f"{anio}-{mes}-{dia}"

    dia_libre = len(horas_ocupadas) == 0

    return render(request, 'reservar_dia.html', {
        'dia': dia,
        'mes': mes,
        'anio': anio,
        'fecha': fecha,
        'reservas': reservas,
        'espacio': espacio,
        'horas_ocupadas': horas_ocupadas,
        'horas_rango': horas_rango,
        'dia_libre': dia_libre
    })

@login_required
@user_passes_test(es_usuario, login_url='reservas_activas')
def reservar_hora(request, pk, month, year, day, hour):
    dia = day
    mes = month
    anio = year

    if anio < datetime.now().year or anio > datetime.now().year+1:
        anio = datetime.now().year

    if mes < 1 or mes > 12 or (anio == datetime.now().year and mes < datetime.now().month):
        mes = datetime.now().month

    if dia < 1 or dia > 31:
        dia = datetime.now().day

    if hour < 9 or hour > 20:
        Http404("Hora no válida")

    fecha = f"{anio}-{mes}-{dia}"

    espacio = EspacioComun.objects.get(pk=pk)

    return render(request, 'reservar_hora.html', {
        'hora': hour,
        'dia': dia,
        'mes': mes,
        'anio': anio,
        'fecha': fecha,
        'espacio': espacio,
    })

@login_required
@user_passes_test(es_usuario, login_url='reservas_activas')
def reservar_dia_entero(request, pk):
    # recibe por post dia, mes, anio

    if request.method == 'POST':
        dia = request.POST.get('dia')
        mes = request.POST.get('mes')
        anio = request.POST.get('anio')

        # comprobar parametros

        if not dia or not mes or not anio:
            Http404("Faltan parámetros")

        if int(dia) < 1 or int(dia) > 31:
            Http404("Día no válido")

        if int(mes) < 1 or int(mes) > 12:
            Http404("Mes no válido")

        fecha_inicio = datetime(int(anio), int(mes), int(dia), 9)
        fecha_fin = fecha_inicio.replace(hour=21)

        reserva = Reserva.objects.create(
            usuario=request.user,
            espacio_comun=EspacioComun.objects.get(pk=pk),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

        # Crear notificación de reserva

        espacio_comun = EspacioComun.objects.get(pk=pk)

        usuario = Usuario.objects.get(user=request.user)

        crear_notificacion(reserva, 'realizada')

        return redirect('mis_reservas')

@login_required
@user_passes_test(es_usuario, login_url='reservas_activas')
def reservar(request, pk):
    # recibe por post dia, mes, anio, hora

    if request.method == 'POST':
        dia = request.POST.get('dia')
        mes = request.POST.get('mes')
        anio = request.POST.get('anio')
        hora = request.POST.get('hora')

        # comprobar parametros

        if not dia or not mes or not anio or not hora:
            Http404("Faltan parámetros")

        if int(dia) < 1 or int(dia) > 31:
            Http404("Día no válido")

        if int(mes) < 1 or int(mes) > 12:
            Http404("Mes no válido")

        if int(hora) < 9 or int(hora) > 20:
            Http404("Hora no válida")


        fecha_inicio = datetime(int(anio), int(mes), int(dia), int(hora))
        fecha_fin = fecha_inicio.replace(hour=fecha_inicio.hour + 1)

        reserva = Reserva.objects.create(
            usuario=request.user,
            espacio_comun=EspacioComun.objects.get(pk=pk),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

        # Crear notificación de reserva
        
        espacio_comun = EspacioComun.objects.get(pk=pk)

        usuario = Usuario.objects.get(user=request.user)

        crear_notificacion(reserva, 'realizada')


        return redirect('mis_reservas')
