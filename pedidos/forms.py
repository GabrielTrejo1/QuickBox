from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Pedido, Ruta

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['direccion', 'codigo_postal']

class RutaForm(forms.ModelForm):
    class Meta:
        model = Ruta
        fields = ['nombre']
