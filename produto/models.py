import os
from django.db import models
from PIL import Image
from django.conf import settings
from django.utils.text import slugify
from utils import utils


class Produto(models.Model):
    name = models.CharField(max_length=50)
    cut_description = models.TextField(max_length=500)
    long_description = models.TextField(max_length=2000)
    image = models.ImageField(
        upload_to='produto_img/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name='preco')
    preco_marketing_promo = models.FloatField(
        default=0, verbose_name='preco_promo')
    tipo = models.CharField(
        max_length=1,
        default='V',
        choices=(
            ('V', 'Variavel'),
            ('S', 'Simples'),
        )
    )

    class Meta:
        verbose_name = ("Produto")
        verbose_name_plural = ("Produtos")

    def get_preco_formatado(self):
        return utils.filter_price(self.preco_marketing)
    get_preco_formatado.short_description = 'Preço'

    def get_preco_formatado_promo(self):
        return utils.filter_price(self.preco_marketing_promo)
    get_preco_formatado_promo.short_description = 'Preço_Promo'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Produto_detail", kwargs={"pk": self.pk})

    @ staticmethod
    def resize_image(img, new_width):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        print(original_width, new_width)
        # valida o tamnho da imagem
        if original_width <= new_width:
            img_pil.close()
            return

        new_height = round((new_width * original_height) / original_width)
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.name)}'
            self.slug = slug

        super().save(*args, **kwargs)  # Call the real save() method
        max_image_size = 500

        if self.image:
            self.resize_image(self.image, max_image_size)


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_marketing = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = ("Variacao")
        verbose_name_plural = ("Variacaos")

    def __str__(self):
        return self.nome or self.produto.name

    def get_absolute_url(self):
        return reverse("Variacao_detail", kwargs={"pk": self.pk})
