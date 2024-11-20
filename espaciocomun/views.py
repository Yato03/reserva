from django.shortcuts import render, get_object_or_404, redirect
from .models import EspacioComun
from django.contrib.auth.decorators import login_required
from datetime import datetime
import calendar
from booking.models import Reserva
from django.http import Http404

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
    month = datetime.now().month
    year = datetime.now().year
    return render(request, 'detalle_espacio_comun.html', {'espacio': espacio, 'imagenes': imagenes, 'month': month, 'year': year})

@login_required
def reserva_espacio_comun(request, pk, month, year):
    """
    Vista para reservar un espacio común.
    """
    # Obtener los días con colores desde la base de datos
    reservas = Reserva.objects.all()
    fechas_colores = {dia.fecha_inicio.date(): 'rojo' for dia in reservas}

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
        'espacio': EspacioComun.objects.get(pk=pk)
    })

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

    reservas = [reserva for reserva in reservas if reserva.fecha_inicio.date() == datetime(anio, mes, dia).date()]

    horas_ocupadas = {reserva.fecha_inicio.hour for reserva in reservas}
    horas_rango = [(hora, hora+1) for hora in range(9, 21)]

    fecha = f"{anio}-{mes}-{dia}"

    return render(request, 'reservar_dia.html', {
        'dia': dia,
        'mes': mes,
        'anio': anio,
        'fecha': fecha,
        'reservas': reservas,
        'espacio': espacio,
        'horas_ocupadas': horas_ocupadas,
        'horas_rango': horas_rango
    })

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

        Reserva.objects.create(
            usuario=request.user,
            espacio_comun=EspacioComun.objects.get(pk=pk),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )

        return redirect('mis_reservas')