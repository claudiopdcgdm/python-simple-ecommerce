# Generated by Django 3.1.4 on 2021-01-05 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='cpf',
            field=models.CharField(help_text='Somente numeros', max_length=11),
        ),
    ]
