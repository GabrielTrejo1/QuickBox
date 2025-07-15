from django import forms
from .models import Contactos

class ContactosForm(forms.ModelForm):
    class Meta:
        model = Contactos
        fields = ['nombre', 'telefono', 'email', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'telefono': forms.TextInput(attrs={'placeholder': 'Teléfono de contacto'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Correo'}),
            'mensaje': forms.Textarea(attrs={'placeholder': 'Mensaje'}),
        }