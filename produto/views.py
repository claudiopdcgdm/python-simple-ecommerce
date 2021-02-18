from django.http import HttpResponse
from pprint import pprint

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib import messages
from .models import Produto, Variacao


class ProdutoList(ListView):
    model = Produto
    template_name = 'produto/produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 6


class ProdutoDetalhes(DetailView):
    model = Produto
    template_name = 'produto/produto_details.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class ProdutoAddToCar(View):

    def get(self, *args, **kwargs):

        # limpa o carinho
        # if self.request.session.get('carrinho'):
        #     del self.request.session['carrinho']
        #     self.request.session.save()

        http_referer = self.request.META.get(
            'HTTP_referer',
            reverse('produto:lista')
        )
        # converti devido a dar erro na jora de remover não encontrarva o id no diccionário
        variacao_id = int(self.request.GET.get('vid'))

        if not variacao_id:
            messages.error(
                self.request, f'Produto não encontrado!!!'
            )
            # pega a pagina que o usuario estava anteriormente
            return redirect(http_referer)

        variacao = get_object_or_404(Variacao, id=variacao_id)
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.name
        variacao_nome = variacao.nome
        # variacao_id = variacao.id
        preco_unitario = variacao.preco or ''
        preco_unitario_promocional = variacao.preco_marketing or ''
        quantidade = 1
        slug = produto.slug
        imagem = produto.image

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Produto Esgotado!!!'
            )
            return redirect(http_referer)

    ################# SESSOIONS #######################
        # criando sessões para guardar os dados
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        carrinho = self.request.session.get('carrinho')

        if variacao_id in carrinho:
            # variacao existe no carrinho
            # obtem quantidade da chave variacao_id
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao.estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque do produto Esgotado!!! {variacao.estoque} {produto.name} adicionados no carrinho'
                )
                return redirect(http_referer)
                # caso a qtd compra seja maior do disponivel em estoque ele adiona a quantidade do estque no carrinho
                # quantidade_carrinho = variacao.estoque
            # atualiza a qtd do valor no dicionario. EX: 1{'quantidade': 'quantidade_carrinho'} /// 1{'quantidade': 4}
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = quantidade_carrinho * preco_unitario
            carrinho[variacao_id]['preco_quantitativo_promocional'] = quantidade_carrinho * \
                preco_unitario_promocional

        else:
            # variacao NÃO existe no carrinho
            carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                'variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_quantitativo':  preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quantitativo_promocional': preco_unitario_promocional,
                'quantidade': quantidade,
                'slug': slug,
                'imagem': imagem,
            }
        self.request.session.save()

        # pprint(carrinho)
        messages.success(
            self.request,
            f'Produto {produto.slug} {variacao.nome} adicionado ao carrrinho'
        )
        return redirect(http_referer)


class ProdutoRemoverFromCar(View):
    def get(self, *args, **kwargs):
        http_refer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:produtoRemoverFromCar')
        )

        variacao_id = self.request.GET.get('vid')

        # when user access from copy/past url
        if not variacao_id:
            return redirect(http_refer)

        # when not itens in sesssion cart
        if not self.request.session.get('carrinho'):
            return redirect(http_refer)

        # when key not exists in dict carrinho
        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_refer)

        carrinho = self.request.session['carrinho'][variacao_id]

        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        messages.success(
            self.request, f'Produto {carrinho["produto_nome"]} removido')
        return redirect(http_refer)


class Cart(View):
    def get(self, *args, **kwargs):
        template = 'produto/cart.html'
        return render(self.request, template)


class Resumo(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagina  Finalizar')
