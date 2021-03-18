from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta


class Pedido(models.Model):

    def deadline():
        current_date = timezone.now()
        delivery_date = current_date + timedelta(days=7)
        return delivery_date

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    create_at = models.DateTimeField(default=timezone.now)
    dt_entrega = models.DateTimeField(default=deadline())
    total = models.FloatField()
    qtd_total = models.PositiveIntegerField()
    status = models.CharField(
        default='C',
        max_length=1,
        choices=(
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Reprovado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        )
    )
    modo_pagto = models.CharField(
        max_length=2,
        default='CC',
        choices=(
                ('CC', 'Cartão Credito'),
                ('BV', 'Boleto a Vista'),
                ('BP', 'Boleto Parcelado'),
                ('CD', 'Cartão Debito'),
                ('VA', 'Vale Troca'),
        )
    )

    class Meta:
        verbose_name = ("Pedido")
        verbose_name_plural = ("Pedidos")

    def __str__(self):
        return (f'Pedido Nro. {self.pk}')


class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=50)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=50)
    variacao_id = models.PositiveIntegerField()
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    quantidade = models.PositiveIntegerField()
    imagem = models.CharField(max_length=2000)

    class Meta:
        verbose_name = ("ItemPedido")
        verbose_name_plural = ("ItemPedidos")

    def __str__(self):
        return (f'Item Pedido. {self.pedido}')
