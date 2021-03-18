
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from pedido.models import Pedido, ItemPedido
from produto.models import Produto, Variacao
from utils import utils
from external.api import Api
from datetime import datetime


class Pagar(View):

    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):

        # verificar se cliente está logado
        if not self.request.user.is_authenticated:
            messages.error(self.request, 'Voce precisa estar logado')
            return redirect('perfil:insert')

        # verfica se carrinho está vazio
        if not self.request.session.get('carrinho'):
            messages.error(self.request, 'Adicione itens ao seu carrinho')
            return redirect('produto:lista')

        # pega a sessão dfo carrinho
        carrinho = self.request.session.get('carrinho')

        # faz um for e pega todas os ids do carrinho
        # para validação e atualização de estoque
        carrinho_variacao_ids = [v for v in carrinho]

        # busca todas as variações no db
        # com as variações obtidas
        bd_variacoes = list(
            Variacao.objects.select_related('produto')
            .filter(id__in=carrinho_variacao_ids)
        )

        # valida estoque e atuazaliza o carrinho
        for variacao in bd_variacoes:
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']

            error_msg_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_quantitativo_promocional'] = estoque * \
                    preco_unt_promo

                error_msg_estoque = 'Estoque insuficiente para alguns '\
                    'produtos do seu carrinho. '\
                    'Reduzimos a quantidade desses produtos. Por favor, '\
                    'verifique quais produtos foram afetados a seguir.'

            if error_msg_estoque:
                messages.error(
                    self.request,
                    error_msg_estoque
                )

                self.request.session.save()
                return redirect('produto:carrinho')

        qtd_total_carrinho = utils.cart_qtd_total(carrinho)
        valor_total_carrinho = utils.cart_totals(carrinho)

        data_context = (
            self.request.user, valor_total_carrinho, qtd_total_carrinho
        )

        contexto = {
            'pedido': data_context
        }

        return render(self.request, self.template_name, contexto)

    def post(self, request, *args, **kwargs):

        data = self.request.POST

        # pagamento via cartão de Crédito
        if data.get('formapagamento') == 'cc':
            titular_cc = data.get('nome_cartao_cc')
            numero_cc = data.get('numero_cartao_cc')
            data_validade_cc = data.get('data_validade_cc')
            codigo_seguranca_cc = data.get('cvv_cc')

            # valida se todos os campos foram enviados
            if not titular_cc or not numero_cc or not data_validade_cc \
                    or not codigo_seguranca_cc:
                messages.error(self.request, 'Dados do cartão incorretos')
                return render(self.request, self.template_name)

            pedido_id = self.salvarPedido('C', 'CC')
            if pedido_id:
                messages.success(
                    self.request, 'Pedido aprovado, obrigado pela compra')
                return redirect('pedido:detalhePedido', pk=pedido_id)
            messages.warning(
                self.request,
                'Escolha um forma de pagamento',
            )
            return render(self.request, self.template_name)

        # pagamento via cartão de debido
        if data.get('formapagamento') == 'cd':
            titular_cd = data.get('nome_cartao_cd')
            numero_cd = data.get('numero_cartao_cd')
            data_validade_cd = data.get('data_validade_cd')
            codigo_seguranca_cd = data.get('senha_cd')

            # valida se todos os campos foram enviados
            if not titular_cd or not numero_cd or not data_validade_cd \
                    or not codigo_seguranca_cd:
                messages.error(self.request, 'Dados do cartão incorretos')
                return render(self.request, self.template_name)

            # chama metodo de salvar pedido
            pedido_id = self.salvarPedido('C', 'CD')
            if pedido_id:
                messages.success(
                    self.request, 'Pedido aprovado, obrigado pela compra')
                return redirect('pedido:detalhePedido', pk=pedido_id)
            messages.error(
                self.request,
                'Erro ao salvar o pedido, Pedido não efetuado!!!'
            )
            return redirect('produto:lista')

        # pagamento via boleto
        if data.get('formapagamento') == 'bo':

            # chama metodo de salvar pedido
            pedido_id = self.salvarPedido('C', 'BV')
            if pedido_id:
                messages.success(
                    self.request, f'Pedido efetuado, enviamos o boleto para pagamento \
                        para o email {self.request.user.email}. Obrigado!!!'
                )
                # return redirect('produto:lista')
                return redirect('pedido:detalhePedido', pk=pedido_id)
            messages.error(
                self.request,
                'Erro ao salvar o pedido, Pedido não efetuado!!!'
            )
            return redirect('produto:lista')

        # pagamento via boleto-parcelado (novo)
        if data.get('formapagamento') == 'bp':

            # chama metodo de salvar pedido
            pedido_id = self.salvarPedido('P', 'BP')

            if pedido_id:
                messages.success(
                    self.request, f'Pedido efetuado, Informaremos quando seu pedido \
                        for aprovado. Obrigado!!!'
                )
                return redirect('pedido:detalhePedido', pk=pedido_id)
            else:
                messages.success(
                    self.request, f'Erro ao inserir dados na api'
                )
                return redirect('produto:lista')

            messages.error(
                self.request,
                'Erro ao salvar o pedido, Pedido não efetuado!!!'
            )
            return redirect('produto:lista')

        # return default
        messages.warning(
            self.request,
            'Escolha um forma de pagamento',
        )
        return render(self.request, self.template_name)

    def salvarPedido(self, status, modoPagto):

        # pega a sessão dfo carrinho
        carrinho = self.request.session.get('carrinho')
        usuario = self.request.user
        qtd_total_carrinho = utils.cart_qtd_total(carrinho)
        valor_total_carrinho = utils.cart_totals(carrinho)

        # # prepara dados para salvar  no banco
        pedido = Pedido(
            usuario=usuario,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status=status,
            modo_pagto=modoPagto
        )

        # salva
        pedido.save()

        # salva itens do pedido no banco
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values()
            ]
        )

        # atualiza dados da api'
        pedido_db = Pedido.objects.filter(id=pedido.id).first()
        str_dt_pedido = pedido_db.create_at.strftime('%Y-%m-%dT%H:%M:%S')
        str_dt_entrega = pedido_db.dt_entrega.strftime('%Y-%m-%dT%H:%M:%S')

        # print(pedido_db)

        data = {
            "id": pedido_db.id,
            "code": pedido_db.id,
            "create_at": str_dt_pedido,
            "deadline": str_dt_entrega,
            "total": pedido_db.total,
            "status": pedido_db.status,
            "payment": pedido_db.modo_pagto,
            "client": pedido_db.usuario.id
        }

        # print(data.get('client'))
        # # instancia da classe Api
        api = Api()
        return_api = api.isPostPedido(data)

        return pedido.id


class SalvarPedido(Pagar):
    def post(self, request, *args, **kwargs):
        return HttpResponse('pagina salvar pedido')


class DetalhePedido(DetailView):
    model = Pedido
    template_name = 'pedido/detalhePedido.html'
    context_object_name = 'pedido'
    pk_url_kwargs = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id_pedido = self.kwargs.get('pk')
        context["itens"] = ItemPedido.objects.filter(
            pedido=id_pedido
        )
        return context

    def get_queryset(self):
        usuario = self.request.user

        if usuario:
            return super().get_queryset()
        return redirect('produto:lista')
