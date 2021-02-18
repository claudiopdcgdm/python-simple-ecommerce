from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from . import models, forms
import copy


class Insert(View):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))

        self.template_name = 'perfil/insert_user.html'

        self.contexto = {
            'userform': forms.UserForm(self.request.POST or None)
        }

        self.user_form = self.contexto.get('userform')

    def get(self, *args, **kwargs):

        if self.request.user.username:
            messages.success(
                self.request, 'Opa, voce ja está logado, aproveita as ofertas')
            return redirect('produto:lista')
        return render(self.request, self.template_name, self.contexto)

    def post(self, *args, **kwargs):
        if not self.user_form.is_valid():
            messages.error(self.request, 'Formulário com erros')
            return render(self.request, self.template_name, self.contexto)

        password = self.user_form.cleaned_data.get('password')
        user = self.user_form.save(commit=False)
        user.set_password(password)
        user.save()

        # loga usuario
        if password:
            authentica = authenticate(
                self.request,
                username=user,
                password=password
            )

        if authentica:
            login(self.request, user=user)

        # mantem o carrinho da sessão

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        return redirect('perfil:register')
        return render(self.request, self.template_name, self.contexto)


class Register(Insert):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.template_name = 'perfil/register.html'

        self.contexto = {
            'perfilform': forms.PerfilForm(self.request.POST or None)
        }

        self.perfil_form = self.contexto.get('perfilform')

    def get(self, request, *args, **kwargs):

        username_logado = self.request.user.username
        id_user_loged = self.request.user.id
        # verifica se usuario nao está logado e manda para pagina de criacao de conta
        if not username_logado:
            messages.error(
                self.request, 'Comece criando sua conta de acesso!!!')
            return redirect('perfil:insert')

        # verifica se usuario jah possui perfil criado
        user_perfil = models.Perfil.objects.filter(usuario_id=id_user_loged)

        if user_perfil:
            messages.error(
                self.request, 'Usuário jah possui perfil criado')
            return redirect('produto:lista')

        return render(self.request, self.template_name, self.contexto)

    def post(self, request, *args, **kwargs):

        if not self.perfil_form.is_valid():
            messages.error(self.request, 'Formulário com erros')
            return render(self.request, self.template_name, self.contexto)

        perfil = self.perfil_form.save(commit=False)
        perfil.usuario = self.request.user
        perfil.save()

        # mantem o carrinho da sessão
        # print(self.carrinho)
        # self.request.session['carrinho'] = self.carrinho
        # self.request.session.save()

        messages.success(
            self.request, 'Cadastro realizado, agora voce pode continuar aproveitando as ofertas, vá em frente')

        return redirect('produto:lista')

        return render(self.request, self.template_name, self.contexto)


class Update(View):

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)

        self.template_name = 'perfil/update_user.html'

        print(self.request.user)
        self.contexto = {
            'userform': forms.UserForm(
                data=self.request.POST or None,
                instance=self.request.user,
            ),
            'perfilform': forms.PerfilForm(
                data=self.request.POST or None,
                instance=self.request.user,
            )
        }

        self.renderizar = render(
            self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class Login(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagina  login')


class Logout(View):
    def get(self, *args, **kwargs):
        return HttpResponse('Pagina logout ')
