from django.urls import path
from . import views

urlpatterns = [
    path('mis_reservas/', views.mis_reservas, name='mis_reservas'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
    path('reservas_activas/', views.reservas_activas, name='reservas_activas'),
    path('finalizar/<int:reserva_id>/', views.finalizar_reserva, name='finalizar_reserva'),
    path('confirmar/<int:reserva_id>/', views.confirmar_reserva, name='confirmar_reserva'),
]