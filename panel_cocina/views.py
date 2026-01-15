from django.shortcuts import render,get_object_or_404,redirect
from restaurante_app.models import Pedidos
# Create your views here.

def panel_cocina_pedidos(request):
    pedidos_domicilios = Pedidos.objects.filter(estado_pedido=False)
    return render(request,'panel_cocina.html',{'pedidos_domicilios':pedidos_domicilios})


def editar_pedido_cocina(request,id):
    pedido_a_confirmar= get_object_or_404(Pedidos,id=id)
    if request.method == 'POST':
        pedido_a_confirmar.estado_pedido = True
        pedido_a_confirmar.save()
        return redirect('panel_cocina')
    
    
    return redirect('panel_cocina')
    
    
        
        
        