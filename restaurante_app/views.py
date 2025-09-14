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
