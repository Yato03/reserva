from django.test import TestCase

# Create your tests here.
# tests.py
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Usuario
from .forms import RegisterForm

class RegisterFormTestCase(TestCase):
    def setUp(self):
        self.valid_data = {
            "dni": "12345678",
            "telefono": "123456789",
            "password": "securepassword123",
            "password_confirm": "securepassword123",
        }

    def test_form_valid_with_matching_passwords(self):
        """El formulario debe ser válido cuando las contraseñas coinciden."""
        form = RegisterForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_with_mismatched_passwords(self):
        """El formulario debe ser inválido cuando las contraseñas no coinciden."""
        invalid_data = self.valid_data.copy()
        invalid_data["password_confirm"] = "differentpassword"
        form = RegisterForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn("Las contraseñas no coinciden.", form.errors["__all__"])

    def test_user_creation_on_save(self):
        """El método save debe crear un usuario vinculado y el modelo Usuario."""
        form = RegisterForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

        # Guardar el formulario
        usuario = form.save()

        # Verificar que el usuario de Django se ha creado
        user = User.objects.get(username=self.valid_data["dni"])
        self.assertEqual(user.username, self.valid_data["dni"])
        self.assertTrue(user.check_password(self.valid_data["password"]))

        # Verificar que el modelo Usuario está asociado correctamente
        self.assertEqual(usuario.dni, self.valid_data["dni"])
        self.assertEqual(usuario.telefono, self.valid_data["telefono"])
        self.assertEqual(usuario.user, user)
