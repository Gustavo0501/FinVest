from django import forms
from .models import Usuario, PerfilFinanceiro
from django.core.exceptions import ValidationError
from django.utils.timezone import now
import re
from decimal import Decimal
from django.utils import timezone
import calendar
import locale

# 🧩 Formulário de Registro de Usuário
class RegistroUsuarioForm(forms.ModelForm):
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

    # 🔍 Validação de CPF
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not cpf.isdigit():
            raise ValidationError("O CPF deve conter apenas números.")
        if len(cpf) != 11:
            raise ValidationError("O CPF deve ter exatamente 11 dígitos.")
        if not self.validar_cpf(cpf):
            raise ValidationError("O CPF informado é inválido.")
        return cpf

    # 🧩 Função para validar o CPF usando o algoritmo de verificação
    def validar_cpf(self, cpf):
        def calcular_digito(cpf, peso):
            soma = sum(int(digito) * (peso - i) for i, digito in enumerate(cpf[:peso - 1]))
            resto = soma % 11
            return '0' if resto < 2 else str(11 - resto)
        primeiro_digito = calcular_digito(cpf, 10)
        segundo_digito = calcular_digito(cpf, 11)
        return cpf[-2:] == primeiro_digito + segundo_digito

    # 🔍 Validação de telefone
    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefone')
        if not telefone.isdigit():
            raise ValidationError("O telefone deve conter apenas números.")
        if len(telefone) != 11:
            raise ValidationError("O telefone deve ter 11 dígitos.")
        return telefone


# 🧩 Formulário de Informações Financeiras
class InformacoesFinanceirasForm(forms.ModelForm):
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
        current_month = calendar.month_name[now.month].capitalize()
        instance.mes_referente = current_month

        if commit:
            instance.save()
        return instance
