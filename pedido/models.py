from django.db import models
from django.contrib.auth.models import User


class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
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
