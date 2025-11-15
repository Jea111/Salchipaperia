from django.urls import path
from .views  import reseñaView


urlpatterns = [
    path('resenas/',reseñaView, name='resenas')
]
