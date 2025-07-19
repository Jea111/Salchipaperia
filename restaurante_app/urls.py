from django.urls import path
from .  import views
from django.conf.urls.static import static


urlpatterns = [
    path('', views.users,name='login'),
    path('inicio/', views.inicio,name='inicio'),
]


