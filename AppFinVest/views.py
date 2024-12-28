import requests
from django.shortcuts import render

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
        return render(request, 'AppFinVest/criptomoedas.html', {'criptomoedas': criptomoedas, 'error_message': error_message})

    return render(request, 'AppFinVest/pages/criptomoedas.html', {'criptomoedas': criptomoedas})