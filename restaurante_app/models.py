from django.db import models
from datetime import datetime
# Create your models here.

class Categorias(models.Model):
    nombre = models.CharField(max_length=200)
    
    def __str__(self):
        return f'Nombre: {self.nombre}'
    class Meta:
        verbose_name = 'Categorias'
        verbose_name_plural = 'Categorias'



class Productos(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion= models.TextField()
    precio =models.DecimalField(decimal_places=2,max_digits=10)
    imagen= models.ImageField(upload_to='media/', null=True, blank=True)
    categoria= models.ForeignKey(Categorias,on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)
    fecha_creado = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.nombre} $ {self.precio}'
    
    class Meta:
        verbose_name = 'Productos'
        verbose_name_plural = 'Productos'
        
class Usuarios(models.Model):
    """Formulario si el pago y la compra se hace por la web y no redireccionado a wpp"""
    
    nombre = models.CharField(max_length=200)
    direccion = models.CharField(max_length=200)
    metodo_pago=models.CharField(max_length=200, choices=[("efectivo", "Efectivo"), ("nequi", "Nequi"), ("Bancolombia", "Bancolombia")])
        
    def __str__(self):
        return f'Usuario: {self.nombre} - Direccion {self.direccion} - Metodo de pago {self.metodo_pago}'
    
class Pedidos(models.Model):
    prodc = models.ForeignKey(Productos,on_delete=models.CASCADE)
    user_pedido = models.ForeignKey(Usuarios,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'USUARIO: {self.user_pedido} DEL PEDIDO {self.prodc}'