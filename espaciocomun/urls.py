from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_espacios_comunes, name='listar_espacios_comunes'),
    path('detalles/<int:pk>/', views.detalle_espacio_comun, name='detalle_espacio_comun'),
    path('reservas/<int:pk>/<int:month>/<int:year>', views.reserva_espacio_comun, name='reserva_espacio_comun'),
    path('reservas/<int:pk>/<int:month>/<int:year>/<int:day>', views.reservar_dia, name='reservar_dia'),
    path('reservas/<int:pk>/<int:month>/<int:year>/<int:day>/<int:hour>', views.reservar_hora, name='reservar_hora'),
    path('reservas/reservar/<int:pk>', views.reservar, name='reservar'),
    path('reservas/reservar_dia_entero/<int:pk>', views.reservar_dia_entero, name='reservar_dia_entero'),
]
