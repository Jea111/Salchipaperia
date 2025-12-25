from django.contrib import admin
from . models import Productos,Usuarios,Pedidos

# Register your models here.
class Produ(admin.ModelAdmin):
    
    fields = ['nombre','descripcion','precio','imagen','precio_descuento','disponible']
    list_display = ['nombre','descripcion','precio','imagen','precio_descuento','disponible','fecha_creado']
    list_filter = ['nombre','descripcion','precio','precio_descuento','disponible','fecha_creado']
    search_fields = ['nombre','descripcion','precio','precio_descuento','disponible','fecha_creado']
    
    
class User(admin.ModelAdmin):
    
    fields = ['nombre','direccion','telefono','metodo_pago']
    list_display = ['nombre','direccion','telefono','metodo_pago']
    list_filter = ['nombre','direccion','telefono','metodo_pago']
    search_fields = ['nombre','direccion','telefono','metodo_pago']
    
class Pedido(admin.ModelAdmin):
    
    fields = ['prodc','user_pedido','total','direccion_envio','metodo_pago','estado_pedido','cantidad']
    list_display = ['prodc','user_pedido','total','direccion_envio','metodo_pago','estado_pedido','cantidad','fecha']
    list_filter = ['prodc','user_pedido','total','direccion_envio','metodo_pago','estado_pedido','cantidad']
    search_fields = ['prodc','user_pedido','total','direccion_envio','metodo_pago','estado_pedido','cantidad']
    
    
admin.site.register(Productos,Produ)
admin.site.register(Pedidos,Pedido)
admin.site.register(Usuarios,User)