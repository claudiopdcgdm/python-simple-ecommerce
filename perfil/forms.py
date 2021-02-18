from django import forms
from django.contrib.auth.models import User
from .models import Perfil
from datetime import date


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=True,
        label='Senha',
        widget=forms.PasswordInput()
    )

    confirm_password = forms.CharField(
        required=True,
        label='Confirmar Senha',
        widget=forms.PasswordInput()
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',
                  'password', 'confirm_password')

    def clean(self, *args, **kwargs):

        cleaned = self.cleaned_data
        fields_validation_error = {}

        first_name_data = cleaned.get('first_name')
        last_name_data = cleaned.get('last_name')
        email_data = cleaned.get('email')
        username_data = cleaned.get('username')
        password_data = cleaned.get('password')
        confirm_password_data = cleaned.get('confirm_password')

        error_email_exists = 'Email jah cadastrado'
        error_user_exists = 'Usuario jah cadastrado'
        error_password_short = 'Senha precisa ser maios que 8 digitos'
        error_password_math = 'Senhas não conferem'
        error_password_null = 'Campo Obrigatório'

        email_db = User.objects.filter(email=email_data).first()
        user_db = User.objects.filter(username=username_data).first()

        if user_db:
            fields_validation_error['username'] = error_user_exists

        if email_db:
            fields_validation_error['email'] = error_email_exists

        if password_data:
            if password_data != confirm_password_data:
                fields_validation_error['confirm_password'] = error_password_math
            if len(password_data) < 8:
                fields_validation_error['password'] = error_password_short

        if fields_validation_error:
            raise(forms.ValidationError(fields_validation_error))


class PerfilForm(forms.ModelForm):

    class Meta:
        model = Perfil
        fields = ("__all__")
        exclude = ('usuario',)

    def clean(self, *args, **kwargs):
        cleaned = self.cleaned_data
        cpf_data = cleaned.get('cpf')
        idade_data = cleaned.get('idade')
        dt_nascimento_data = cleaned.get('data_nascimento')
        dt_atual = date.today()
        fields_error_validate = {}

        cpf_db = Perfil.objects.filter(cpf=cpf_data).first()

        # # verifica se o cpf jah está cadastrado
        # if cpf_db:
        #     fields_error_validate['cpf'] = 'CPF jah Cadastrado'

        # verifica se a idade correponde a data de nascimento
        idade = abs((dt_atual.year - dt_nascimento_data.year))
        if idade != idade_data:
            fields_error_validate[
                'data_nascimento'] = f'Idade não corresponde a data de nascimento, idade{idade}'

        if fields_error_validate:
            raise (forms.ValidationError(fields_error_validate))
