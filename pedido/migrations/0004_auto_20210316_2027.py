# Generated by Django 3.1.7 on 2021-03-16 23:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0003_auto_20210316_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='dt_entrega',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 23, 20, 27, 3, 567592)),
        ),
    ]
