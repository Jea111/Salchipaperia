from django.urls import path
from .  import views

urlpatterns = [
    path('', views.users,name='login'),
    path('inicio/', views.inicio,name='inicio'),
    path('procesar-pedido/', views.procesar_pedido, name='procesar_pedido'),


]