from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    
    path('color/azul/', views.color_azul, name='color_azul'),
    path('color/rojo/', views.color_rojo, name='color_rojo'),
    path('color/amarillo/', views.color_amarillo, name='color_amarillo'),
    path('color/morado/', views.color_morado, name='color_morado'),
    path('ministerio/<int:id>/', views.ministerio_detalle, name='ministerio_detalle'),
    path('Nuestro_origen/', views.Nuestro_origen, name='Nuestro_origen'),
    path('Nuestra_casa/', views.Nuestra_casa, name='Nuestra_casa'),
]