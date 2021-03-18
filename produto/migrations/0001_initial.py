# Generated by Django 3.1.4 on 2020-12-16 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('cut_description', models.CharField(max_length=50)),
                ('long_description', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='produto_img/%Y/%m')),
                ('slug', models.SlugField(unique=True)),
                ('preco_marketing', models.FloatField()),
                ('preco_marketing_promo', models.FloatField(default=0)),
                ('tipo', models.CharField(choices=[('V', 'Variação'), ('S', 'Simples')], default='V', max_length=1)),
            ],
        ),
    ]
