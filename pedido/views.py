from django.shortcuts import render
from django.views import View
from django.http import HttpResponse


class Pagar(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagina Pagamento')


class SalvarPedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagina Fechar Pedido')


class DetalhePedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagina Detalhe Pedido ')
