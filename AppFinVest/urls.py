from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('visao-geral/', views.visao_geral),
    path('acoes/', views.stock_table),
    path('criptomoedas/', views.criptomoedas),
    path('graficos/', views.graficos),
    path('registro/', views.registro_etapa1, name='registro'),
    path('registro/informacoes-financeiras', views.registro_etapa2, name='registroFinanceiro'),
    path('registro/informacoes-financeiras/info-perfil-investidor', views.infoPerfilInvestidor, name='infoPerfilInvestidor'),
    path('registro/informacoes-financeiras/info-perfil-endividado', views.infoPerfilEndividado, name='infoPerfilEndividado'),
]
