from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Usuarios, Productos, Pedidos,Categorias
import json

def users(request):
    """La validación es solo practica,pq un cliente puede tener varios pedidos y deberiamos requerir que la zona sea solo en itagui y prado"""
    productos = Productos.objects.all()
    
    if request.method == 'POST':
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        metodo_pago = request.POST['metodo_pago']

        userExist = Usuarios.objects.filter(nombre=nombre).exists()
        
        if userExist:
            return JsonResponse({'mensaje': 'El usuario ya existe'}, status=400)
        else:
            Usuarios.objects.create(
                nombre=nombre, 
                direccion=direccion, 
                metodo_pago=metodo_pago
            )
            return redirect('inicio')

    return render(request, 'login.html', {
        'productos': productos
    })

def inicio(request):
    prods = Productos.objects.all()
    return render(request, 'inicio.html', {
        'prod': prods
    })




# def descuont(request):
#     newDescuento = 10 * 100 / 100
    
#     return render (request,'inicio.html',{'descuento': newDescuento})
        
        

# def pedidosRealizados(request):
#     if request.method == 'POST':
#         usuario_id = request.POST.get('user_id')
#         productos_ids = request.POST.getlist('producto_id')  # lista de IDs

#         usuario = get_object_or_404(Usuarios, id=usuario_id)

#         for pid in productos_ids:
#             producto = get_object_or_404(Productos, id=pid)
#             Pedidos.objects.create(user=usuario, produ=producto)

#         return JsonResponse({'mensaje': 'Pedido confirmado'})
    
#     return JsonResponse({'error': 'Método no permitido'}, status=405)
