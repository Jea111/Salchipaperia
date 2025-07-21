from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Usuarios, Productos
import json

def users(request):
    productos = Productos.objects.all()
    
    if request.method == 'POST':
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        metodo_pago = request.POST['metodo_pago']
        
        Usuarios.objects.create(nombre=nombre, direccion=direccion, metodo_pago=metodo_pago)
        return redirect('inicio')
    
    return render(request, 'login.html', {
        'productos': productos
    })

def inicio(request):
    prods = Productos.objects.all()
    return render(request, 'inicio.html', {
        'prod': prods
    })

@csrf_exempt
def procesar_pedido(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            carrito = data.get('carrito', [])

            if not carrito:
                return JsonResponse({'error': 'Carrito vacío'}, status=400)

            for item in carrito:
                producto_id = item['id']
                cantidad = item['cantidad']
                
                try:
                    producto = Productos.objects.get(id=producto_id)
                    print(f"Pedido recibido: {producto.nombre} x {item.cantidad}")
                except Productos.DoesNotExist:
                    return JsonResponse({'error': f'Producto ID {producto_id} no existe'}, status=404)

            return JsonResponse({'mensaje': 'Pedido procesado correctamente'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'JSON inválido'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)
