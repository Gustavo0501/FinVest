from django import forms
from .models import Usuario, PerfilFinanceiro
from django.core.exceptions import ValidationError
from django.utils.timezone import now
import re
from decimal import Decimal
from django.utils import timezone
import calendar
import locale
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password


class FormularioBaseValidacao(forms.Form):
    # Validação do nome de usuário
    def validar_nome_usuario(self, nome_usuario):
        if not nome_usuario:
            raise ValidationError("O nome de usuário é obrigatório.")
        if len(nome_usuario) < 3:
            raise ValidationError("O nome de usuário deve ter pelo menos 3 caracteres.")
        return nome_usuario

    # Validação do e-mail
    def validar_email(self, email):
        if not email:
            raise ValidationError("O e-mail é obrigatório.")
        if '@' not in email:
            raise ValidationError("Informe um e-mail válido.")
        return email

    # Validação do CPF
    def validar_cpf(self, cpf):
        if not cpf.isdigit():
            raise ValidationError("O CPF deve conter apenas números.")
        if len(cpf) != 11:
            raise ValidationError("O CPF deve ter exatamente 11 dígitos.")
        if not self.validar_cpf(cpf):
            raise ValidationError("O CPF informado é inválido.")
        return cpf

    # Validação de telefone
    def validar_telefone(self, telefone):
        if not telefone.isdigit():
            raise ValidationError("O telefone deve conter apenas números.")
        if len(telefone) != 11:
            raise ValidationError("O telefone deve ter 11 dígitos.")
        return telefone

    # Função auxiliar para validar CPF
    def validar_cpf(self, cpf):
        if not cpf.isdigit():
            raise ValidationError("O CPF deve conter apenas números.")
        if len(cpf) != 11:
            raise ValidationError("O CPF deve ter exatamente 11 dígitos.")

        def calcular_digito(cpf, peso):
            soma = sum(int(digito) * (peso - i) for i, digito in enumerate(cpf[:peso - 1]))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)

        primeiro_digito = calcular_digito(cpf, 10)
        segundo_digito = calcular_digito(cpf, 11)

        if cpf[-2:] != primeiro_digito + segundo_digito:
            raise ValidationError("O CPF informado é inválido.")

        return cpf


# 🧩 Formulário de Registro de Usuário
class FormularioRegistroUsuario(FormularioBaseValidacao, forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'primeiro_nome',
            'ultimo_nome',
            'nome_usuario',
            'email',
            'senha',
            'cpf',
            'telefone',
            'data_nascimento',
        ]
        widgets = {
            'primeiro_nome': forms.TextInput(attrs={"class": "form-control", "placeholder": "Primeiro Nome"}),
            'ultimo_nome': forms.TextInput(attrs={"class": "form-control", "placeholder": "Último Nome"}),
            'nome_usuario': forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome de Usuário"}),
            'email': forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-mail"}),
            'senha': forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Senha"}),
            'cpf': forms.TextInput(attrs={"class": "form-control", "placeholder": "CPF (somente números)"}),
            'telefone': forms.TextInput(attrs={"class": "form-control", "placeholder": "Telefone (somente números)"}),
            'data_nascimento': forms.DateInput(attrs={"class": "form-control", "placeholder": "Data de Nascimento", "type": "date"}),
        }

    def clean_nome_usuario(self):
        return self.validar_nome_usuario(self.cleaned_data.get('nome_usuario'))

    def clean_email(self):
        return self.validar_email(self.cleaned_data.get('email'))

    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        return self.validar_cpf(cpf)

    def clean_telefone(self):
        return self.validar_telefone(self.cleaned_data.get('telefone'))

# 🧩 Formulário de Informações Financeiras
class FormularioInfoFinanceiras(forms.ModelForm):
    class Meta:
        model = PerfilFinanceiro
        fields = ['renda', 'divida', 'patrimonio']

    # 🔍 Validação dos campos numéricos
    def clean(self):
        cleaned_data = super().clean()
        renda = cleaned_data.get('renda')
        divida = cleaned_data.get('divida')
        patrimonio = cleaned_data.get('patrimonio')

        if renda is not None and renda < 0:
            self.add_error('renda', "A renda não pode ser negativa.")
        if divida is not None and divida < 0:
            self.add_error('divida', "A dívida não pode ser negativa.")
        if patrimonio is not None and patrimonio < 0:
            self.add_error('patrimonio', "O patrimônio não pode ser negativo.")

        return cleaned_data

    # 🧩 Função para calcular o tipo de perfil
    def calcular_tipo_perfil(self):
        renda = self.cleaned_data.get('renda') 
        divida = self.cleaned_data.get('divida') 
        if renda is None or divida is None: 
            return "Indeterminado" 
        # Usando float diretamente para os cálculos 
        if divida > (renda * Decimal(0.5)): 
            return "Endividado" 
        return "Investidor"

    # 🔧 Sobrescrevendo o método save()
    def save(self, usuario, commit=True):
        instance = super().save(commit=False)
        instance.usuario = usuario
        instance.tipo_perfil = self.calcular_tipo_perfil()

        # 🔧 Define o mês referente com base no timezone
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        
        now = timezone.now()
        mes_atual = calendar.month_name[now.month].capitalize()
        instance.mes_referente = mes_atual

        if commit:
            instance.save()
        return instance

class FormularioLogin(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-mail"}),
        error_messages={
            "required": "O campo e-mail é obrigatório.",
            "invalid": "Informe um e-mail válido.",
        },
    )
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Senha"}),
        error_messages={"required": "O campo senha é obrigatório."},
    )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not Usuario.objects.filter(email=email).exists():
            raise ValidationError("Nenhum usuário encontrado com este e-mail.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        senha = cleaned_data.get("senha")

        if email and senha:
            try:
                # Verifica se o usuário existe
                usuario = Usuario.objects.get(email=email)
                # Valida a senha usando o hash salvo no banco
                if not check_password(senha, usuario.senha):
                    raise ValidationError("A senha está incorreta.")
            except Usuario.DoesNotExist:
                raise ValidationError("Credenciais inválidas.")
        return cleaned_data

class FormularioPerfilUsuario(FormularioBaseValidacao, forms.ModelForm): 
    class Meta: 
        model = Usuario
        fields = [
            'primeiro_nome', 
            'ultimo_nome', 
            'nome_usuario', 
            'cpf', 
            'telefone', 
            'data_nascimento', 
            'email'
        ]

        widgets = {
            'primeiro_nome': forms.TextInput(attrs={"class": "form-control"}),
            'ultimo_nome': forms.TextInput(attrs={"class": "form-control"}),
            'nome_usuario': forms.TextInput(attrs={"class": "form-control"}),
            'cpf': forms.TextInput(attrs={"class": "form-control"}),
            'telefone': forms.TextInput(attrs={"class": "form-control"}),
            'data_nascimento': forms.DateInput(attrs={"class": "form-control", "type": "date"}, format='%Y-%m-%d'),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean_nome_usuario(self):
        return self.validar_nome_usuario(self.cleaned_data.get('nome_usuario'))

    def clean_email(self):
        return self.validar_email(self.cleaned_data.get('email'))

    def clean_cpf(self):
        return self.validar_cpf(self.cleaned_data.get('cpf'))

    def clean_telefone(self):
        return self.validar_telefone(self.cleaned_data.get('telefone'))


class FormularioMudarSenha(forms.Form):
    senha_antiga = forms.CharField(widget=forms.PasswordInput, label='Senha Atual')
    nova_senha1 = forms.CharField(widget=forms.PasswordInput, label='Nova Senha')
    nova_senha2 = forms.CharField(widget=forms.PasswordInput, label='Confirmar Nova Senha')

    def __init__(self, *args, **kwargs):
        self.Usuario = kwargs.pop('Usuario', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        senha_antiga = cleaned_data.get('senha_antiga')
        nova_senha1 = cleaned_data.get('nova_senha1')
        nova_senha2 = cleaned_data.get('nova_senha2')

        if not self.Usuario.check_password(senha_antiga):
            self.add_error('senha_antiga', 'Senha atual incorreta.')
        
        if nova_senha1 and nova_senha1 != nova_senha2:
            self.add_error('nova_senha2', 'As novas senhas não coincidem.')

        return cleaned_data

    def save(self, commit=True):
        nova_senha = self.cleaned_data.get('nova_senha1')
        self.Usuario.senha = make_password(nova_senha)
        if commit:
            self.Usuario.save()
        return self.Usuario
