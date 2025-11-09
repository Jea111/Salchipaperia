from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from django.db import transaction
from .models import Usuarios, Productos, Pedidos
from decimal import Decimal, InvalidOperation
import json
import logging
import urllib.parse
from django.conf import settings

logger = logging.getLogger(__name__)

def inicio(request):
    prods = Productos.objects.all()
    return render(request, 'inicio.html', {
        'prod': prods
    })


def format_whatsapp_message(usuario, productos_pedido, total_pedido):
    """Formatea el mensaje de WhatsApp con los detalles del pedido."""
    mensaje = f" *NUEVO PEDIDO*\n\n"
    mensaje += f"*Cliente:* {usuario.nombre}\n"
    mensaje += f"*Teléfono:* {usuario.telefono}\n"
    mensaje += f"*Dirección:* {usuario.direccion}\n"
    mensaje += f"*Método de Pago:* {usuario.metodo_pago}\n\n"
    
    mensaje += "*Productos:*\n"
    for pedido in productos_pedido:
        mensaje += f"- {pedido.prodc.nombre} × {pedido.cantidad} = ${pedido.total}\n"
    
    mensaje += f"\n*TOTAL: ${total_pedido}*"
    return mensaje

def pedidosUser(request):
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nomb = request.POST.get('nombre', '').strip()
            direc = request.POST.get('direccion', '').strip()
            tel = request.POST.get('telefono', '').strip()
            met_p = request.POST.get('metodo_pago', '').strip()
            carrito = request.POST.get('carrito', '').strip()

            # Validar campos requeridos
            campos_requeridos = {
                'Nombre': nomb,
                'Dirección': direc,
                'Teléfono': tel,
                'Método de pago': met_p,
                'Carrito': carrito
            }

            campos_faltantes = [campo for campo, valor in campos_requeridos.items() if not valor]
            
            if campos_faltantes:
                return HttpResponseBadRequest(
                    f'Los siguientes campos son requeridos: {", ".join(campos_faltantes)}'
                )

            # Validar formato del carrito
            try:
                productos = json.loads(carrito)
                if not productos:
                    return HttpResponseBadRequest('El carrito está vacío')
                    
                # Validar estructura de cada item del carrito
                for item in productos:
                    if not isinstance(item, dict):
                        return HttpResponseBadRequest('Formato de item inválido')
                    if 'id' not in item:
                        return HttpResponseBadRequest('ID de producto requerido')
                    if 'cantidad' not in item:
                        return HttpResponseBadRequest('Cantidad requerida')
                
                # Inicializar lista para almacenar los pedidos
                pedidos_lista = []
                        
            except json.JSONDecodeError:
                return HttpResponseBadRequest('Formato de carrito inválido')

            with transaction.atomic():
                usuario = Usuarios.objects.create(
                    nombre=nomb, direccion=direc, telefono=tel, metodo_pago=met_p
                )

                for item in productos:
                    try:
                        # Usar id del producto 
                        prod_id = item.get('id')
                        if not prod_id:
                            raise ValueError('ID de producto requerido')
                            
                        produc_pedido = Productos.objects.get(id=prod_id)
                        cantidad = int(item.get('cantidad', 1))
                        if cantidad < 1:
                            raise ValueError('Cantidad debe ser positiva')
                            
                        # Usar precio del producto en BD
                        total_item = produc_pedido.precio * cantidad

                        pedido = Pedidos.objects.create(
                            user_pedido=usuario,
                            prodc=produc_pedido,
                            cantidad=cantidad,
                            total=total_item
                        )
                        pedidos_lista.append(pedido)
                    except Productos.DoesNotExist:
                        raise ValueError(f'Producto {prod_id} no existe')
                    except (TypeError, ValueError) as e:
                        raise ValueError(f'Error en item del carrito: {str(e)}')

            # Calcular total del pedido
            total_pedido = sum(pedido.total for pedido in pedidos_lista)
            
            # Formatear y enviar mensaje de WhatsApp
            mensaje = format_whatsapp_message(usuario, pedidos_lista, total_pedido)
            whatsapp_numero = "3147681762"
            whatsapp_url = f"https://wa.me/{whatsapp_numero}?text={urllib.parse.quote(mensaje)}"
                        
            return render(request, 'confirmacion.html', {
                'usuario': usuario,
                'pedidos': pedidos_lista,
                'total': total_pedido,
                'whatsapp_url': whatsapp_url
            })
                        
        except json.JSONDecodeError:
            logger.error('Error decodificando carrito JSON')
            return HttpResponseBadRequest('Formato de carrito inválido')
        except ValueError as e:
            logger.error(f'Error validando pedido: {str(e)}')
            return HttpResponseBadRequest(str(e))
        except Exception as e:
            logger.exception('Error inesperado procesando pedido')
            return HttpResponseBadRequest('Error procesando pedido')

        return render(request, 'confirmacion.html', {'usuario': usuario})

    return render(request, 'login.html')
