# Generated by Django 3.1.7 on 2021-03-17 18:31

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0006_auto_20210317_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='dt_entrega',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 24, 18, 31, 2, 945, tzinfo=utc)),
        ),
    ]
