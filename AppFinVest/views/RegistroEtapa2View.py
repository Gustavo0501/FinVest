from datetime import datetime
from django.views import View
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from AppFinVest.decorators import registro_required
from AppFinVest.models import Usuario
from AppFinVest.formularios import FormularioInfoFinanceiras
from django.contrib.auth.hashers import make_password
from decimal import Decimal

class RegistroEtapa2View(View):
    template_name = 'AppFinVest/pages/registro_etapa2.html'

    @method_decorator(registro_required)
    def get(self, request):
        if 'registro_dados' not in request.session:
            return redirect('registro')
        form = FormularioInfoFinanceiras()
        return render(request, self.template_name, {'form': form})

    @method_decorator(registro_required)
    def post(self, request):
        if 'registro_dados' not in request.session:
            return redirect('registro')

        dados_pessoais = request.session.get('registro_dados')
        dados_pessoais['data_nascimento'] = datetime.strptime(dados_pessoais['data_nascimento'], '%Y-%m-%d').date()

        form = FormularioInfoFinanceiras(request.POST)
        if form.is_valid():
            usuario = Usuario.objects.filter(email=dados_pessoais['email']).first()
            if not usuario:
                usuario = Usuario(
                    primeiro_nome=dados_pessoais['primeiro_nome'],
                    ultimo_nome=dados_pessoais['ultimo_nome'],
                    nome_usuario=dados_pessoais['nome_usuario'],
                    cpf=dados_pessoais['cpf'],
                    telefone=dados_pessoais['telefone'],
                    data_nascimento=dados_pessoais['data_nascimento'],
                    email=dados_pessoais['email'],
                    senha=make_password(dados_pessoais['senha']),
                )
                usuario.save()

            perfil_financeiro = form.save(usuario=usuario)
            usuario.tipo_perfil = perfil_financeiro.tipo_perfil
            usuario.save()

            # Obtenha os valores do formulário como Decimal
            renda = Decimal(form.cleaned_data.get('renda'))
            divida = Decimal(form.cleaned_data.get('divida'))
            patrimonio = Decimal(form.cleaned_data.get('patrimonio'))

            # Lógica para decidir o perfil
            if divida > patrimonio or renda < divida * Decimal(0.5):
                return redirect('infoPerfilEndividado')  # Perfil Endividado
            else:
                return redirect('infoPerfilInvestidor')  # Perfil Investidor

        return render(request, self.template_name, {'form': form})
