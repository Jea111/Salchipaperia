from django.shortcuts import render,redirect
from .models import Usuarios,Productos
# Create your views here.
def users(request):
    productos = Productos.objects.all()
    
    if request.method == 'POST':
        nombre = request.POST['nombre']
        direccion = request.POST['direccion']
        metodo_pago = request.POST['metodo_pago']
        
        Usuarios.objects.create(nombre=nombre,direccion=direccion,metodo_pago=metodo_pago)
        return redirect('inicio')
    return render(request,'login.html',{
            'productos':productos
        })




def inicio(request):
    prods = Productos.objects.all()
    return render(request,'inicio.html',{
        'prod':prods
    })