from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.utils import timezone
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.generic import DeleteView
from django.contrib.auth.models import User
from . import models, forms
from external.api import Api
import copy


class Insert(View):

    template_name = 'perfil/insert_user.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        self.perfil = None

        if self.request.user.is_authenticated:
            self.perfil = models.Perfil.objects.filter(
                usuario=self.request.user
            ).first()

            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil
                )
            }
        else:
            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None
                )
            }

        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        self.renderizar = render(
            self.request, self.template_name, self.contexto
        )

    def get(self, *args, **kwargs):
        return self.renderizar

    def post(self, *args, **kwargs):
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            messages.error(
                self.request,
                'Existem erros no formulário de cadastro. Verifique se todos '
                'os campos foram preenchidos corretamente.'
            )

            return self.renderizar

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')

        # Usuário logado (atualiza)
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(
                User, username=self.request.user.username)

            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            """
            verifica se usuário logado tem perfil criado
            se não tiver, pega os dados do formaulzario de perfil
            e grava no banco passado o usuario_id
            """
            if not self.perfil:
                self.perfilform.cleaned_data['usuario'] = usuario
                print(self.perfilform.cleaned_data)
                perfil = models.Perfil(**self.perfilform.cleaned_data)
                perfil.save()
            else:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

            """
            Implementação da API- methodo PUT
            """

            api = Api()
            return_api = api.isGetCliente()
            return_end = api.isGetEndereco()

            # obtem o id da lista de dicionários
            self.id_user = None
            for item in return_api:
                if item['code'] == str(usuario.id):
                    self.id_user = item.get('id')
                    break

            # obtem id do endereço
            self.id_endereco = None
            for item in return_end:
                if item['code'] == str(perfil.id):
                    self.id_endereco = item.get('id')
                    break

            self.data = {
                "id": self.id_user,
                "name": f'{usuario.first_name} {usuario.last_name}',
                "code": usuario.id,
                "cpf": perfil.cpf,
                "email": usuario.email,
                "fone": perfil.fone,
                "create_at": "2021-03-17T20:46:46-03:00",
                "endereco": [
                    self.id_endereco
                ]
            }

            # exucuta o PUT na api
            api.isPutCliente(self.data, self.id_user)

        # Usário não logado (novo)
        else:

            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

            """
            
            Implementação da API- methodo POST
            Executa metodo post da api
            apos gravar dados no banco local,
            faz um POST na api
            http://127.0.0.1:8000/api/apiendereco/ e
            http://127.0.0.1:8000/api/apiclientes/

            """
            api = Api()

            self.data_endereco = {
                "id": perfil.id,
                "code": perfil.id,
                "street": perfil.endereco,
                "number": perfil.numero,
                "complement": perfil.complemento,
                "district": perfil.bairro,
                "city": perfil.cidade,
                "state": perfil.estado,
                "zip_code": perfil.cep,
                "delivery": True
            }

            return_api_josn = api.isPostEndereco(self.data_endereco)
            # print('resultado da api endereco')
            # print(return_api_josn)
            str_create_at = usuario.date_joined.strftime('%Y-%m-%dT%H:%M:%S')

            if return_api_josn:
                self.data_cliente = {
                    "id": perfil.id,
                    'name': f'{usuario.first_name} {usuario.last_name}',
                    "code": usuario.id,
                    "cpf": perfil.cpf,
                    "email": usuario.email,
                    "fone": perfil.fone,
                    "create_at": str_create_at,
                    "endereco": [return_api_josn.get('id')]
                }

                api.isPostCliente(self.data_cliente)

        # faz login do usuário
        if password:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password
            )

            if autentica:
                login(self.request, user=usuario)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        messages.success(
            self.request,
            'Seu cadastro foi criado ou atualizado com sucesso.'
        )

        return redirect('produto:cart')
        return self.renderizar


class Register(Insert):
    pass


class Update(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Atualizar')


class Login(View):
    def get(self, *args, **kwargs):
        return redirect('perfil:insert')

    def post(self, request, *args, **kwargs):
        user = self.request.POST.get('usuario')
        senha = self.request.POST.get('senha')

        if not user or not senha:
            messages.error(self.request, 'Usuário e senha invalidos')
            return redirect('perfil:login')

        usuario = authenticate(self.request, username=user, password=senha)

        if not usuario:
            messages.error(self.request, 'Usuário e senha invalidos')
            return redirect('perfil:login')
        login(self.request, user=usuario)
        return redirect('produto:lista')


class Logout(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('produto:lista')


class PerfilDeleteView(DeleteView):
    model = models.User
    template_name = "perfil/delete.html"
    context_object_name = 'usuario'

    def get_success_url(self):
        usuario = self.get_object()

        """
        executa metodo GET para obter o id do cliente
        """
        api = Api()
        return_api = api.isGetCliente()

        # obtem o id da lista de dicionários
        self.id_user = None
        for item in return_api:
            if item['code'] == str(usuario.id):
                self.id_user = item.get('id')
                break

        api.isDeleteCliente(self.id_user)

        messages.success(
            self.request, f": (- sentiremos sua falta {usuario.first_name} {usuario.last_name}"
        )
        return reverse_lazy("produto:lista")
