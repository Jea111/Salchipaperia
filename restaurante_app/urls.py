from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('pedidos/', views.pedidosUser, name='pedidos'),
]
