from django.contrib import admin
from .models import Produto, Variacao


class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1


class ProdutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cut_description', 'slug',
                    'get_preco_formatado', 'get_preco_formatado_promo', 'tipo')
    list_display_links = ('id', 'name',)
    # list_editable = ('get_preco_formatado','get_preco_formatado_promo', 'tipo')
    inlines = [
        VariacaoInline
    ]


admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao)
