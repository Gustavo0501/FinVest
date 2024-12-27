from django.shortcuts import render

def login(request):
    return render(request, 'AppFinvest/pages/login.html')

def visao_geral(request):
    return render(request, 'AppFinVest/pages/visao-geral.html')
