from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseBadRequest
from django.db import transaction
from decimal import Decimal
import urllib.parse, logging

from .models import Usuarios, Productos, Pedidos

logger = logging.getLogger(__name__)


def _get_cart_from_session(request):
    return request.session.get('cart', {})


def _save_cart_to_session(request, cart):
    request.session['cart'] = cart
    request.session.modified = True


def inicio(request):
    productos = Productos.objects.all()
    cart = _get_cart_from_session(request)

    cart_items = []
    cart_count = 0
    cart_total = Decimal('0.00')

    for pid, qty in cart.items():
        try:
            producto = Productos.objects.get(id=int(pid))
            cantidad = int(qty)
            subtotal = producto.precio * cantidad

            cart_items.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })

            cart_count += cantidad
            cart_total += subtotal
        except Productos.DoesNotExist:
            pass

    return render(request, 'inicio.html', {
        'prod': productos,
        'cart_items': cart_items,
        'cart_count': cart_count,
        'cart_total': cart_total,
    })


def add_to_cart(request, product_id):
    if request.method != 'POST':
        return redirect('inicio')

    get_object_or_404(Productos, id=product_id)
    cart = _get_cart_from_session(request)

    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    _save_cart_to_session(request, cart)

    return redirect(request.META.get('HTTP_REFERER', 'inicio'))


def remove_from_cart(request, product_id):
    if request.method != 'POST':
        return redirect('view_cart')

    cart = _get_cart_from_session(request)
    cart.pop(str(product_id), None)
    _save_cart_to_session(request, cart)

    return redirect('view_cart')


def view_cart(request):
    cart = _get_cart_from_session(request)
    items = []
    total = Decimal('0.00')

    for pid, qty in cart.items():
        try:
            producto = Productos.objects.get(id=int(pid))
            cantidad = int(qty)
            subtotal = producto.precio * cantidad

            items.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })

            total += subtotal
        except Productos.DoesNotExist:
            pass

    return render(request, 'carrito.html', {
        'items': items,
        'total': total,
    })
def confirm_cart(request):
    cart = _get_cart_from_session(request)

    if not cart:
        return HttpResponseBadRequest('El carrito está vacío')

    if request.method != 'POST':
        return redirect('view_cart')

    nomb = request.POST.get('nombre', '').strip()
    direc = request.POST.get('direccion', '').strip()
    tel = request.POST.get('telefono', '').strip()
    met_p = request.POST.get('metodo_pago', '').strip()

    if not all([nomb, direc, tel, met_p]):
        return HttpResponseBadRequest('Todos los campos son obligatorios')

    with transaction.atomic():

        usuario = Usuarios.objects.filter(telefono=tel).first()

        if not usuario:
            usuario = Usuarios.objects.create(
                nombre=nomb,
                direccion=direc,
                telefono=tel,
                metodo_pago=met_p
            )

        pedidos_lista = []

        for pid, qty in cart.items():
            producto = Productos.objects.get(id=int(pid))
            cantidad = int(qty)
            total_item = producto.precio * cantidad

            pedido_existente = Pedidos.objects.filter(
                user_pedido=usuario,
                prodc=producto,
                estado_pedido=False
            ).first()

            if pedido_existente:
                pedido_existente.cantidad += cantidad
                pedido_existente.total += total_item
                pedido_existente.save()
                pedidos_lista.append(pedido_existente)
            else:
                pedido = Pedidos.objects.create(
                    user_pedido=usuario,
                    prodc=producto,
                    cantidad=cantidad,
                    total=total_item,
                    direccion_envio=direc,
                    metodo_pago=met_p
                )
                pedidos_lista.append(pedido)

    request.session['cart'] = {}
    request.session.modified = True

    total_pedido = sum(p.total for p in pedidos_lista)

    mensaje = (
        f"*NO MODIFICAR ESTE MENSAJE*\n\n"
        f"*Cliente:* {usuario.nombre}\n"
        f"Pedido confirmado\n"
        f"Tu pedido llegará en 25 minutos\n"
        f"Gracias por tu compra\n"
    )

    whatsapp_url = (
        "https://wa.me/573147681762?text="
        + urllib.parse.quote(mensaje)
    )

    return render(request, 'confirmacion.html', {
        'usuario': usuario,
        'pedidos': pedidos_lista,
        'total': total_pedido,
        'whatsapp_url': whatsapp_url
    })
