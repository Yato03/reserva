from django.urls import path

from . import views

urlpatterns = [
    path('registro/', views.registrar_usuario, name='registro'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil_usuario, name='perfil'),
    path('notificaciones/', views.mis_notificaciones, name='mis_notificaciones'),
    path('editar_perfil/', views.editar_perfil, name='editar_perfil'),
]
