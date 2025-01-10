import requests
from django.shortcuts import render, redirect
from AppFinVest.models import PerfilFinanceiro
from AppFinVest.models import Usuario
import json
from django.utils import timezone
import calendar
import locale
from AppFinVest.models import PrecoAtivo, TabelaGlobal, Observer
from AppFinVest.formularios import RegistroUsuarioForm, InformacoesFinanceirasForm
from django.contrib.auth.hashers import make_password
from datetime import datetime

def login(request):
    return render(request, 'AppFinvest/pages/login.html')

# View para a primeira etapa do registro (dados pessoais)
def registro_etapa1(request):
    print(request.method)
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            # Armazena os dados pessoais na sessão
            dados_pessoais = form.cleaned_data
            dados_pessoais['data_nascimento'] = str(dados_pessoais['data_nascimento'])  # Convertendo para string
            request.session['registro_dados'] = dados_pessoais
            return redirect('registroFinanceiro') #view registro_etapa2

        if not form.is_valid():
            print(form.errors)
    else:
        form = RegistroUsuarioForm()
    return render(request, 'AppFinVest/pages/registro_etapa1.html', {'form': form})


# View para a segunda etapa do registro (informações financeiras)
def registro_etapa2(request):
    action_form = 'registroFinanceiro'
    # Verifica se os dados pessoais estão presentes na sessão
    dados_pessoais = request.session.get('registro_dados')
    if not dados_pessoais:
        # Se não houver dados pessoais, redireciona para a primeira etapa
        return redirect('registro')

    if request.method == 'POST':
        form = InformacoesFinanceirasForm(request.POST)
        if form.is_valid():
            # Cria o usuário com as informações da sessão
            usuario = Usuario(
                primeiro_nome=dados_pessoais['primeiro_nome'],
                ultimo_nome=dados_pessoais['ultimo_nome'],
                nome_usuario=dados_pessoais['nome_usuario'],
                cpf=dados_pessoais['cpf'],
                telefone=dados_pessoais['telefone'],
                data_nascimento=datetime.strptime(dados_pessoais['data_nascimento'], '%Y-%m-%d').date(),  # Convertendo de string para date
                email=dados_pessoais['email'],
                senha=make_password(dados_pessoais['senha']),
            )

            usuario.save()

            # Define o tipo de perfil com base nas informações financeiras
            # Salva as informações financeiras 
            perfil_financeiro = form.save(usuario=usuario)

            # Atualiza o tipo de perfil do usuário 
            usuario.tipo_perfil = perfil_financeiro.tipo_perfil 
            usuario.save()
            
            # O tipo de perfil já foi calculado no método save do formulário 
            if perfil_financeiro.tipo_perfil == 'Endividado': 
                return redirect('infoPerfilEndividado') 
            else: 
                return redirect('infoPerfilInvestidor')



    else:
        form = InformacoesFinanceirasForm()
    return render(request, 'AppFinVest/pages/registro_etapa2.html', {'form': form})

def infoPerfilInvestidor(request):
    return render(request, 'AppFinVest/pages/perfilInvestidor.html')

def infoPerfilEndividado(request):
    return render(request, 'AppFinVest/pages/perfilEndividado.html')

def visao_geral(request):
    return render(request, 'AppFinVest/pages/visao-geral.html')


def stock_table(request):
    tabela_global = TabelaGlobal.get_instance()
    stock_data = [
        {
            "symbol": acao.nome_ativo,
            "date": acao.data,
            "open_price": acao.abertura,
            "high_price": acao.maximo,
            "low_price": acao.minimo,
            "close_price": acao.fechamento,
            "volume": acao.volume,
        }
        for acao in tabela_global.get_acoes()
    ]
    
    return render(request, 'AppFinVest/pages/acoes.html', {'stock_data': stock_data})


def criptomoedas(request):
    tabela_global = TabelaGlobal.get_instance()
    cripto_data = [
        {
            "name": cripto.nome_ativo,
            "current_price": cripto.preco_atual,
            "market_cap": cripto.capitalizacao_mercado,
            "total_volume": cripto.volume_24h,
        }
        for cripto in tabela_global.get_criptomoedas()
    ]
    
    return render(request, 'AppFinVest/pages/criptomoedas.html', {'criptomoedas': cripto_data})

def graficos(request):
    # Simulando o usuário logado (substitua com `request.user` se o sistema de autenticação estiver configurado)
    usuario_logado = Usuario.objects.first()  # Pega o primeiro usuário como exemplo

    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    
    # Obtém o mês e o ano atuais
    now = timezone.now()
    current_month = calendar.month_name[now.month].capitalize()

    # Filtra os registros financeiros do usuário logado para o mês atual
    registro_usuario = PerfilFinanceiro.objects.filter(
        usuario=usuario_logado,
        mes_referente=current_month,
    )

    # Obtém o último registro, se existir
    ultimo_registro = registro_usuario.first()

    # Se a requisição for um POST, atualiza os dados
    if request.method == 'POST':
        renda = request.POST.get('renda')
        divida = request.POST.get('divida')
        patrimonio = request.POST.get('patrimonio')

        # Atualiza ou cria o registro
        if ultimo_registro:
            ultimo_registro.renda = renda
            ultimo_registro.divida = divida
            ultimo_registro.patrimonio = patrimonio
            ultimo_registro.save()
        else:
            PerfilFinanceiro.objects.create(
                usuario=usuario_logado,
                tipo_perfil=usuario_logado.tipo_perfil,
                mes_referente=current_month,
                renda=renda,
                divida=divida,
                patrimonio=patrimonio
            )
    
    if ultimo_registro:
        renda_atual=json.dumps(float(ultimo_registro.renda))
        divida_atual=json.dumps(float(ultimo_registro.divida))
        patrimonio_atual=json.dumps(float(ultimo_registro.patrimonio))

    else:
        renda_atual=json.dumps(0.0)
        divida_atual=json.dumps(0.0)
        patrimonio_atual=json.dumps(0.0)

    #=====================================================================
    # Filtrando as informações financeiras do usuário logado
    infos_financeiras = PerfilFinanceiro.objects.filter(usuario=usuario_logado).order_by('mes_referente')

    # Lista de meses em ordem
    meses = [
        "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
        "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
    ]

    # Inicializando dicionários para armazenar os dados agrupados por mês
    dados_patrimonio = {mes: [] for mes in meses}
    dados_renda = {mes: [] for mes in meses} 
    dados_divida = {mes: [] for mes in meses} 

    # Preenchendo os dicionários com os valores financeiros
    for info in infos_financeiras:
        dados_patrimonio[info.mes_referente] = float(info.patrimonio)
        dados_renda[info.mes_referente] = float(info.renda)
        dados_divida[info.mes_referente] = float(info.divida)

    # Transformando os dicionários em listas que o gráfico possa entender
    patrimonio = [dados_patrimonio[mes] for mes in meses]
    renda = [dados_renda[mes] for mes in meses]
    dividas = [dados_divida[mes] for mes in meses]

    #===============================================================

    context = {
        "usuario": usuario_logado,
        "meses": json.dumps(meses),  # Serializando para JSON
        "patrimonio": json.dumps(patrimonio),
        "renda": json.dumps(renda),
        "dividas": json.dumps(dividas),
        "renda_atual": renda_atual,
        "divida_atual": divida_atual,
        "patrimonio_atual": patrimonio_atual,
    }

    return render(request, 'AppFinVest/pages/graficos.html', context)