from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro_etapa1, name='registro'),
    path('registro/informacoes-financeiras', views.registro_etapa2, name='registroFinanceiro'),
    path('registro/informacoes-financeiras/info-perfil-investidor', views.infoPerfilInvestidor, name='infoPerfilInvestidor'),
    path('registro/informacoes-financeiras/info-perfil-endividado', views.infoPerfilEndividado, name='infoPerfilEndividado'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/mudar-senha', views.mudar_senha, name='mudar_senha'),
    path('excluir-conta/', views.excluir_conta, name='excluir_conta'),
    path('visao-geral/', views.visao_geral, name='visao-geral'),
    path('acoes/', views.tabela_acoes),
    path('criptomoedas/', views.criptomoedas),
    path('graficos/', views.graficos),
]
