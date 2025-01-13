from django.urls import path

from .views import (
    LoginView, LogoutView, RegistroEtapa1View, RegistroEtapa2View, InfoPerfilInvestidorView,
    InfoPerfilEndividadoView, PerfilView, MudarSenhaView, ExcluirContaView,
    TabelaAcoesView, CriptomoedasView, GraficosView, VisaoGeralView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', RegistroEtapa1View.as_view(), name='registro'),
    path('registro/informacoes-financeiras', RegistroEtapa2View.as_view(), name='registroFinanceiro'),
    path('registro/informacoes-financeiras/info-perfil-investidor', InfoPerfilInvestidorView.as_view(), name='infoPerfilInvestidor'),
    path('registro/informacoes-financeiras/info-perfil-endividado', InfoPerfilEndividadoView.as_view(), name='infoPerfilEndividado'),
    path('perfil/', PerfilView.as_view(), name='perfil'),
    path('perfil/mudar-senha', MudarSenhaView.as_view(), name='mudar_senha'),
    path('excluir-conta/', ExcluirContaView.as_view(), name='excluir_conta'),
    path('visao-geral/', VisaoGeralView.as_view(), name='visao-geral'),
    path('acoes/', TabelaAcoesView.as_view(), name='tabela_acoes'),
    path('criptomoedas/', CriptomoedasView.as_view(), name='criptomoedas'),
    path('graficos/', GraficosView.as_view(), name='graficos'),
]
