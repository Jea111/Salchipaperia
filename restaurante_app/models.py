from django.db import models
from decimal import Decimal

class Productos(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(decimal_places=2, max_digits=10)
    precio_descuento = models.DecimalField(decimal_places=2, max_digits=10)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    disponible = models.BooleanField(default=True)
    fecha_creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} - ${self.precio}'


class Usuarios(models.Model):
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    telefono = models.CharField(max_length=50,unique=True)
    metodo_pago = models.CharField(max_length=200)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.nombre} ({self.metodo_pago})'


class Pedidos(models.Model):
    user_pedido = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    prodc = models.ForeignKey(Productos, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    total = models.DecimalField(decimal_places=2, max_digits=10)
    
    direccion_envio = models.CharField(max_length=200)
    metodo_pago = models.CharField(max_length=200)
    
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_pedido.nombre} - {self.prodc.nombre}'
