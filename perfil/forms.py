from django import forms
from django.contrib.auth.models import User
from . import models
from datetime import date

# class UpdateUserForm(forms.ModelForm):
#     # password = forms.CharField(
#     #     required=False,
#     #     label='Senha',
#     #     widget=forms.PasswordInput()
#     # )

#     # confirm_password = forms.CharField(
#     #     required=False,
#     #     label='Confirmar Senha',
#     #     widget=forms.PasswordInput()
#     # )

#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'username')

# class UserForm(forms.ModelForm):
#     password = forms.CharField(
#         required=True,
#         label='Senha',
#         widget=forms.PasswordInput()
#     )

#     confirm_password = forms.CharField(
#         required=True,
#         label='Confirmar Senha',
#         widget=forms.PasswordInput()
#     )

#     class Meta:
#         model = User
#         fields = ('first_name', 'last_name', 'email', 'username',
#                   'password', 'confirm_password')

#     def clean(self, *args, **kwargs):

#         cleaned = self.cleaned_data
#         fields_validation_error = {}

#         first_name_data = cleaned.get('first_name')
#         last_name_data = cleaned.get('last_name')
#         email_data = cleaned.get('email')
#         username_data = cleaned.get('username')
#         password_data = cleaned.get('password')
#         confirm_password_data = cleaned.get('confirm_password')

#         error_email_exists = 'Email jah cadastrado'
#         error_user_exists = 'Usuario jah cadastrado'
#         error_password_short = 'Senha precisa ser maios que 8 digitos'
#         error_password_math = 'Senhas não conferem'
#         error_password_null = 'Campo Obrigatório'

#         email_db = User.objects.filter(email=email_data).first()
#         user_db = User.objects.filter(username=username_data).first()

#         if user_db:
#             fields_validation_error['username'] = error_user_exists

#         if email_db:
#             fields_validation_error['email'] = error_email_exists

#         if password_data:
#             if password_data != confirm_password_data:
#                 fields_validation_error['confirm_password'] = error_password_math
#             if len(password_data) < 8:
#                 fields_validation_error['password'] = error_password_short

#         if fields_validation_error:
#             raise(forms.ValidationError(fields_validation_error))


# class PerfilForm(forms.ModelForm):

#     class Meta:
#         model = Perfil
#         fields = ("__all__")
#         exclude = ('usuario',)

#     def clean(self, *args, **kwargs):
#         cleaned = self.cleaned_data
#         cpf_data = cleaned.get('cpf')
#         idade_data = cleaned.get('idade')
#         dt_nascimento_data = cleaned.get('data_nascimento')
#         dt_atual = date.today()
#         fields_error_validate = {}

#         cpf_db = Perfil.objects.filter(cpf=cpf_data).first()

#         # # verifica se o cpf jah está cadastrado
#         # if cpf_db:
#         #     fields_error_validate['cpf'] = 'CPF jah Cadastrado'

#         # verifica se a idade correponde a data de nascimento
#         # idade = abs((dt_atual.year - dt_nascimento_data.year))
#         # if idade != idade_data:
#         #     fields_error_validate[
#         #         'data_nascimento'] = f'Idade não corresponde a data de nascimento, idade{idade}'

#         if fields_error_validate:
#             raise (forms.ValidationError(fields_error_validate))


class PerfilForm(forms.ModelForm):
    class Meta:
        model = models.Perfil
        fields = '__all__'
        exclude = ('usuario',)


class UserForm(forms.ModelForm):
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
    )

    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação senha'
    )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password',
                  'password2', 'email')

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_msgs = {}

        usuario_data = cleaned.get('username')
        email_data = cleaned.get('email')
        password_data = cleaned.get('password')
        password2_data = cleaned.get('password2')

        usuario_db = User.objects.filter(username=usuario_data).first()
        email_db = User.objects.filter(email=email_data).first()

        error_msg_user_exists = 'Usuário já existe'
        error_msg_email_exists = 'E-mail já existe'
        error_msg_password_match = 'As duas senhas não conferem'
        error_msg_password_short = 'Sua senha precisa de pelo menos 6 caracteres'
        error_msg_required_field = 'Este campo é obrigatório.'

        # Usuários logados: atualização
        if self.usuario:
            if usuario_db:
                if usuario_data != usuario_db.username:
                    validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                if email_data != email_db.email:
                    validation_error_msgs['email'] = error_msg_email_exists

            if password_data:
                if password_data != password2_data:
                    validation_error_msgs['password'] = error_msg_password_match
                    validation_error_msgs['password2'] = error_msg_password_match

                if len(password_data) < 6:
                    validation_error_msgs['password'] = error_msg_password_short

        # Usuários não logados: cadastro
        else:
            if usuario_db:
                validation_error_msgs['username'] = error_msg_user_exists

            if email_db:
                validation_error_msgs['email'] = error_msg_email_exists

            if not password_data:
                validation_error_msgs['password'] = error_msg_required_field

            if not password2_data:
                validation_error_msgs['password2'] = error_msg_required_field

            if password_data != password2_data:
                validation_error_msgs['password'] = error_msg_password_match
                validation_error_msgs['password2'] = error_msg_password_match

            if len(password_data) < 6:
                validation_error_msgs['password'] = error_msg_password_short

        if validation_error_msgs:
            raise(forms.ValidationError(validation_error_msgs))
