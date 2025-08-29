from django.urls import path
from .  import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.users,name='login'),
    path('inicio/', views.inicio,name='inicio'),
    path('procesar-pedido/', views.procesar_pedido, name='procesar_pedido'),


]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)