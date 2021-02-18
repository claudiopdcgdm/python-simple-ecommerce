# Generated by Django 3.1.4 on 2020-12-29 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='produto',
            options={'verbose_name': 'Produto', 'verbose_name_plural': 'Produtos'},
        ),
        migrations.CreateModel(
            name='Variacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True)),
                ('preco', models.FloatField()),
                ('preco_marketing', models.FloatField(default=0)),
                ('estoque', models.PositiveIntegerField(default=1)),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produto.produto')),
            ],
            options={
                'verbose_name': 'Variacao',
                'verbose_name_plural': 'Variacaos',
            },
        ),
    ]