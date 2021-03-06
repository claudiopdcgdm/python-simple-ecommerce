# Generated by Django 3.1.7 on 2021-03-16 23:26

import datetime
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0002_pedido_qtd_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='codigo',
            field=models.CharField(default=0, max_length=50, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pedido',
            name='create_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='pedido',
            name='dt_entrega',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 23, 20, 26, 4, 809970)),
        ),
        migrations.AddField(
            model_name='pedido',
            name='modo_pagto',
            field=models.CharField(choices=[('CC', 'Cartão Credito'), ('BV', 'Boleto a Vista'), ('BP', 'Boleto Parcelado'), ('CD', 'Cartão Debito'), ('VA', 'Vale Troca')], default='CC', max_length=2),
        ),
    ]
