from django.urls import path
from . import views

urlpatterns = [
    path('espacios/', views.listar_espacios_comunes, name='listar_espacios_comunes'),
    path('espacios/<int:pk>/', views.detalle_espacio_comun, name='detalle_espacio_comun'),
]
