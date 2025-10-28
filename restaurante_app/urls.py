from django.urls import path
from .  import views

urlpatterns = [
    path('', views.users,name='login'),
    path('inicio/', views.inicio,name='inicio'),
    # path('pedidos/', views.pedidosRealizados, name='pedidoRealizados'),

]