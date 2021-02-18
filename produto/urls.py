from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ProdutoList.as_view(), name='lista'),
    path('<slug>', views.ProdutoDetalhes.as_view(), name='produtoDetalhes'),
    path('ProdutoAddToCar/', views.ProdutoAddToCar.as_view(), name='produtoAddToCar'),
    path('ProdutoRemoverFromCar/', views.ProdutoRemoverFromCar.as_view(),
         name='produtoRemoverFromCar'),
    path('Cart/', views.Cart.as_view(), name='cart'),
    path('Resumo/', views.Resumo.as_view(), name='resumo'),
]
