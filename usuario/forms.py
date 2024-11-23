from django import forms
from .models import Usuario
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
     # Campo adicional para crear el usuario vinculado
    password = forms.CharField(
        required=True,
        label="Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
    password_confirm = forms.CharField(
        required=True,
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirmar Contraseña'})
    )

    class Meta:
        model = Usuario
        fields = ['dni', 'telefono']

        widgets = {
            'dni': forms.TextInput(attrs={'placeholder': 'DNI'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
        }

        labels = {
            'dni': 'DNI',
            'telefono': 'Número de Teléfono (opcional)',
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")
        if password != password_confirm:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data

    def save(self, commit=True):
        # Crear el usuario vinculado
        user = User(
            username=self.cleaned_data['dni'],
            email=f"{self.cleaned_data['dni']}@example.com"
        )
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()

        # Asociar el usuario al modelo Usuario
        usuario = super().save(commit=False)
        usuario.user = user
        if commit:
            usuario.save()
        return usuario