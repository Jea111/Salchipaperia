from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from .models import Productos, Usuarios, Pedidos
import json

class ProductosTests(TestCase):
    def setUp(self):
        self.producto = Productos.objects.create(
            nombre='Salchipapa Clásica',
            descripcion='La mejor salchipapa',
            precio=Decimal('12000.00'),
            precio_descuento=Decimal('10000.00')
        )

    def test_str_representation(self):
        self.assertEqual(
            str(self.producto),
            'Salchipapa Clásica - $12000.00'
        )

class ViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.producto = Productos.objects.create(
            nombre='Salchipapa Especial',
            descripcion='Salchipapa con todo',
            precio=Decimal('15000.00'),
            precio_descuento=Decimal('13000.00')
        )

    def test_inicio_view(self):
        response = self.client.get(reverse('inicio'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inicio.html')
        self.assertIn('prod', response.context)
        self.assertIn(self.producto, response.context['prod'])

class PedidosTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.producto = Productos.objects.create(
            nombre='Salchipapa Test',
            descripcion='Para pruebas',
            precio=Decimal('10000.00'),
            precio_descuento=Decimal('9000.00')
        )

    def test_crear_pedido_exitoso(self):
        data = {
            'nombre': 'Cliente Test',
            'direccion': 'Calle Test 123',
            'telefono': '3001234567',
            'metodo_pago': 'efectivo',
            'carrito': json.dumps([{
                'id': self.producto.id,
                'cantidad': 2
            }])
        }
        response = self.client.post(reverse('pedidos'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'confirmacion.html')
        
        # Verificar que se creó el pedido
        self.assertEqual(Usuarios.objects.count(), 1)
        self.assertEqual(Pedidos.objects.count(), 1)
        
        pedido = Pedidos.objects.first()
        self.assertEqual(pedido.cantidad, 2)
        self.assertEqual(pedido.total, Decimal('20000.00'))

    def test_crear_pedido_carrito_invalido(self):
        data = {
            'nombre': 'Cliente Test',
            'direccion': 'Calle Test 123',
            'telefono': '3001234567',
            'metodo_pago': 'efectivo',
            'carrito': 'no-es-json'
        }
        response = self.client.post(reverse('pedidos'), data)
        self.assertEqual(response.status_code, 400)
        
        # Verificar que no se creó nada en BD
        self.assertEqual(Usuarios.objects.count(), 0)
        self.assertEqual(Pedidos.objects.count(), 0)

    def test_crear_pedido_producto_inexistente(self):
        data = {
            'nombre': 'Cliente Test',
            'direccion': 'Calle Test 123',
            'telefono': '3001234567',
            'metodo_pago': 'efectivo',
            'carrito': json.dumps([{
                'id': 99999,  # ID que no existe
                'cantidad': 1
            }])
        }
        response = self.client.post(reverse('pedidos'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(Usuarios.objects.count(), 0)
        self.assertEqual(Pedidos.objects.count(), 0)
