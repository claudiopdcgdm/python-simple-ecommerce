from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('pagar/', views.Pagar.as_view(), name='pagar'),
    path('salvarPedido/', views.SalvarPedido.as_view(), name='salvarPedido'),
    path('detalhePedido/<int:pk>',
         views.DetalhePedido.as_view(), name='detalhePedido'),
]
