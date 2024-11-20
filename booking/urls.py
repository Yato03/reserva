from django.urls import path
from . import views

urlpatterns = [
    path('mis_reservas/', views.mis_reservas, name='mis_reservas'),
    path('cancelar/<int:reserva_id>/', views.cancelar_reserva, name='cancelar_reserva'),
]