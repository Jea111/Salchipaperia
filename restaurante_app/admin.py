from django.contrib import admin
from . models import Categorias,Productos,Usuarios,Pedidos

# Register your models here.
class Produ(admin.ModelAdmin):
    
    fields = ['nombre','descripcion','precio','imagen','categoria','disponible']
    list_display = ['nombre','descripcion','precio','imagen','categoria','disponible','fecha_creado']
    list_filter = ['nombre','descripcion','precio','categoria','disponible','fecha_creado']
    search_fields = ['nombre','descripcion','precio','categoria','disponible','fecha_creado']
    
    
class User(admin.ModelAdmin):
    
    fields = ['nombre','direccion','metodo_pago']
    list_display = ['nombre','direccion','metodo_pago']
    list_filter = ['nombre','direccion','metodo_pago']
    search_fields = ['nombre','direccion','metodo_pago']
    
class Pedido(admin.ModelAdmin):
    
    fields = ['prodc','user_pedido']
    list_display = ['prodc','user_pedido']
    list_filter = ['prodc','user_pedido']
    search_fields = ['prodc','user_pedido']
    
    
admin.site.register(Productos,Produ)
admin.site.register(Pedidos,Pedido)
admin.site.register(Usuarios,User)
admin.site.register(Categorias)