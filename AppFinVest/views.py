import requests
from django.shortcuts import render
from AppFinVest.models import PerfilFinanceiro
from AppFinVest.models import Usuario
import json
from django.utils import timezone
import calendar
import locale

def login(request):
    return render(request, 'AppFinvest/pages/login.html')

def visao_geral(request):
    return render(request, 'AppFinVest/pages/visao-geral.html')


# Substitua por sua chave da API Alpha Vantage
API_KEY = 'M7L5Q0TYVCPN6P1K'

# Lista de 10 ativos escolhidos
STOCK_LIST = ["PETR4.SA", "VALE3.SA", "ITUB4.SA", "BBDC4.SA", "ABEV3.SA", 
              "MGLU3.SA", "BBAS3.SA", "GGBR4.SA", "WEGE3.SA", "RENT3.SA"]

def stock_table(request):
    stock_data = []
    error_message = None

    for symbol in STOCK_LIST:
        api_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
        response = requests.get(api_url)

        if response.status_code == 200:
            data = response.json()
            if "Time Series (Daily)" in data:
                # Obtém a data mais recente
                latest_date = next(iter(data["Time Series (Daily)"]))
                values = data["Time Series (Daily)"][latest_date]

                stock_data.append({
                    "symbol": symbol,
                    "date": latest_date,
                    "open_price": values["1. open"],
                    "high_price": values["2. high"],
                    "low_price": values["3. low"],
                    "close_price": values["4. close"],
                    "volume": values["5. volume"],
                })
            else:
                stock_data.append({
                    "symbol": symbol,
                    "error": "Dados não disponíveis"
                })
        else:
            error_message = "Erro ao conectar-se à API."

    return render(request, 'AppFinVest/pages/acoes.html', {'stock_data': stock_data, 'error_message': error_message})


def criptomoedas(request):
    # URL da API CoinGecko para obter dados de criptomoedas
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',  # Moeda de referência
        'order': 'market_cap_desc',  # Ordenar por capitalização de mercado
        'per_page': 10,  # Número de criptomoedas
        'page': 1,
        'sparkline': False  # Não incluir gráfico sparkline
    }

    try:
        # Chamada à API CoinGecko
        response = requests.get(url, params=params)
        response.raise_for_status()
        criptomoedas = response.json()
    except requests.exceptions.RequestException as e:
        criptomoedas = []
        error_message = f"Erro ao buscar dados: {str(e)}"
        return render(request, 'AppFinVest/pages/criptomoedas.html', {'criptomoedas': criptomoedas, 'error_message': error_message})

    return render(request, 'AppFinVest/pages/criptomoedas.html', {'criptomoedas': criptomoedas})


def graficos(request):
    # Simulando o usuário logado (substitua com `request.user` se o sistema de autenticação estiver configurado)
    usuario_logado = Usuario.objects.first()  # Pega o primeiro usuário como exemplo

    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    
    # Obtém o mês e o ano atuais
    now = timezone.now()
    current_month = calendar.month_name[now.month+1].capitalize()

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