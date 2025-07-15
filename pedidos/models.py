from django.db import models
from django.contrib.auth.models import User

class Ruta(models.Model):
  id_ruta = models.AutoField(primary_key=True)
  nombre = models.CharField(max_length=200)
  fecha = models.DateField(auto_now_add=True)
  # ? fecha_fin para saber cuando se Termino la ruta.
  id_usuario = models.ForeignKey('auth.user', on_delete=models.CASCADE)
  estado = models.CharField(max_length=20, choices=[
    ('Activa', 'Activa'),
    ('Cancelada', 'Cancelada'),
    ('Terminada', 'Terminada')
  ], default='Activa')
  inicio = models.CharField(max_length=255, null=True, blank=True)

  def __str__(self):
    return self.nombre

    
class Pedido(models.Model):
  id_pedido = models.AutoField(primary_key=True)
  id_usuario = models.ForeignKey(User, on_delete=models.CASCADE)
  id_ruta = models.ForeignKey(Ruta, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos')
  direccion = models.CharField(max_length=255)
  codigo_postal = models.CharField(max_length=10) # api para obtener el CP de la localidad
  latitud = models.FloatField(null=True, blank=True)
  longitud = models.FloatField(null=True, blank=True)
  fecha_carga = models.DateTimeField(auto_now_add=True)
  estado = models.CharField(max_length=20, choices=[
    ('Pendiente', 'Pendiente'),
    ('Entregado', 'Entregado'),
  ], default='Pendiente')
  
  def __str__(self):
    return f"{self.id_usuario} - {self.direccion}"

