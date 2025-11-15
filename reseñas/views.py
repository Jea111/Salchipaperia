from django.shortcuts import render, get_object_or_404,redirect
from . models import ReseñaSite
# Create your views here.

def reseñaView(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        
        ReseñaSite.objects.create(email=email,message=message)
        return redirect('inicio')
    return render (request,'reseñas.html')