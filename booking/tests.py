from datetime import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from usuario.models import Usuario, Notificacion
from espaciocomun.models import EspacioComun
from booking.models import Reserva
import uuid

class ReservaViewsTest(TestCase):
    def setUp(self):
        # Crear usuarios con roles definidos en Usuario y generar un DNI único
        unique_dni_sereno = str(uuid.uuid4().int)[:8]  # Generar DNI único
        self.sereno_user = User.objects.create_user(username='sereno', password='password')
        self.sereno = Usuario.objects.create(
            user=self.sereno_user,
            dni=unique_dni_sereno,
            rol=Usuario.RolChoices.SERENO,
            telefono="123456789"
        )

        unique_dni_usuario = str(uuid.uuid4().int)[:8]  # Generar DNI único
        self.usuario_user = User.objects.create_user(username='usuario', password='password')
        self.usuario = Usuario.objects.create(
            user=self.usuario_user,
            dni=unique_dni_usuario,
            rol=Usuario.RolChoices.USUARIO,
            telefono="987654321"
        )

        # Crear un espacio común
        self.espacio_comun = EspacioComun.objects.create(nombre="Sala de Reuniones",capacidad=20)

        # Crear reservas
        self.reserva_pendiente = Reserva.objects.create(
            usuario=self.usuario_user,
            espacio_comun=self.espacio_comun,
            fecha_inicio="2024-12-01 10:00:00",
            fecha_fin="2024-12-01 12:00:00",
            estado=Reserva.EstadoChoices.PENDIENTE
        )
        self.reserva_confirmada = Reserva.objects.create(
            usuario=self.usuario_user,
            espacio_comun=self.espacio_comun,
            fecha_inicio="2024-12-02 10:00:00",
            fecha_fin="2024-12-02 12:00:00",
            estado=Reserva.EstadoChoices.CONFIRMADA
        )
        
    def tearDown(self):
        """
        Limpia después de cada prueba.
        Elimina las reservas y espacios comunes creados durante las pruebas.
        """
        print(" limpiando objetos...")
        Reserva.objects.all().delete()  # Elimina todas las reservas
        EspacioComun.objects.all().delete()  # Elimina todos los espacios comunes
        Usuario.objects.all().delete()  # Elimina los usuarios de prueba
        
    def test_reservas_activas(self):
        # Iniciar sesión como 'sereno' y acceder a la vista de reservas activas
        self.client.login(username='sereno', password='password')
        response = self.client.get(reverse('reservas_activas'))

        # Verificar que las reservas activas se muestran correctamente
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reservas Activas')
        self.assertContains(response, self.reserva_pendiente.espacio_comun.nombre)
        self.assertContains(response, self.reserva_confirmada.espacio_comun.nombre)
        self.assertContains(response, self.reserva_pendiente.estado)

    def test_confirmar_reserva(self):
        # Iniciar sesión como 'sereno' y confirmar una reserva pendiente
        self.client.login(username='sereno', password='password')
        response = self.client.get(reverse('confirmar_reserva', args=[self.reserva_pendiente.id]))

        # Verificar que el estado de la reserva cambió a 'CONFIRMADA'
        self.reserva_pendiente.refresh_from_db()
        self.assertEqual(self.reserva_pendiente.estado, Reserva.EstadoChoices.CONFIRMADA)
        self.assertRedirects(response, reverse('reservas_activas'))

    def test_cancelar_reserva(self):
        # Iniciar sesión como 'usuario' y cancelar su propia reserva
        self.client.login(username='usuario', password='password')
        response = self.client.get(reverse('cancelar_reserva', args=[self.reserva_confirmada.id]))

        # Verificar que el estado de la reserva cambió a 'CANCELADA'
        self.reserva_confirmada.refresh_from_db()
        self.assertEqual(self.reserva_confirmada.estado, Reserva.EstadoChoices.CANCELADA)
        self.assertRedirects(response, reverse('mis_reservas'))

    def test_finalizar_reserva(self):
        # Iniciar sesión como 'sereno' y finalizar una reserva confirmada
        self.client.login(username='sereno', password='password')
        response = self.client.get(reverse('finalizar_reserva', args=[self.reserva_confirmada.id]))

        # Verificar que el estado de la reserva cambió a 'FINALIZADA'
        self.reserva_confirmada.refresh_from_db()
        self.assertEqual(self.reserva_confirmada.estado, Reserva.EstadoChoices.FINALIZADA)
        self.assertRedirects(response, reverse('reservas_activas'))

    def test_mis_reservas(self):
        # Iniciar sesión como 'usuario' y acceder a sus propias reservas
        self.client.login(username='usuario', password='password')
        response = self.client.get(reverse('mis_reservas'))

        # Verificar que el usuario vea sus reservas activas
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Mis reservas')
        self.assertContains(response, self.reserva_pendiente.espacio_comun.nombre)
        self.assertContains(response, self.reserva_confirmada.espacio_comun.nombre)

    def test_reserva_en_dia_pasado(self):
        """
        Test que verifica que no se puede reservar un día pasado.
        """
        hoy = datetime.now().date()
        dia_pasado = hoy.replace(year=2023)  # Cambiar el año para que sea un día pasado

        url = reverse('reservar_dia_entero', args=[self.espacio_comun.pk])
        data = {
            'dia': dia_pasado.day,
            'mes': dia_pasado.month,
            'anio': dia_pasado.year
        }
        response = self.client.post(url, data)

        # Verifica que no se ha creado ninguna reserva salvo las que ya hay
        self.assertEqual(Reserva.objects.count(), 2)

    def test_reserva_fuera_de_hora(self):
        """
        Test que verifica que no se puede reservar fuera del horario permitido (9 AM - 8 PM).
        """
        fecha_fuera_de_hora = datetime.now().replace(hour=8, minute=0)  # Antes de las 9 AM

        url = reverse('reservar', args=[self.espacio_comun.pk])
        data = {
            'dia': fecha_fuera_de_hora.day,
            'mes': fecha_fuera_de_hora.month,
            'anio': fecha_fuera_de_hora.year,
            'hora': fecha_fuera_de_hora.hour
        }
        response = self.client.post(url, data)

        # Verifica que no se ha creado ninguna reserva, salvo las 2 q h¡ya hay
        self.assertEqual(Reserva.objects.count(), 2)
        

    def test_reserva_espacio_completo(self):
        """
        Test que verifica que no se puede reservar un espacio completo.
        """
        # Crea una reserva para el espacio en el mismo día y hora
        dia = datetime.now().day
        mes = datetime.now().month
        anio = datetime.now().year

        reserva_existente = Reserva.objects.create(
            usuario=self.usuario.user,
            espacio_comun=self.espacio_comun,
            fecha_inicio=datetime(anio, mes, dia, 9),
            fecha_fin=datetime(anio, mes, dia, 10)
        )

        # Intentamos hacer una nueva reserva en el mismo horario
        url = reverse('reservar', args=[self.espacio_comun.pk])
        data = {
            'dia': dia,
            'mes': mes,
            'anio': anio,
            'hora': 9
        }
        response = self.client.post(url, data)

        # Verifica que no se ha creado una nueva reserva, salvo als existentes y la inicial
        self.assertEqual(Reserva.objects.count(), 3)
        
