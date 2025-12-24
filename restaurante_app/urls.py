from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('carrito/', views.view_cart, name='view_cart'),
    path('agregar/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('eliminar/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('confirmar/', views.confirm_cart, name='confirm_cart'),
]
