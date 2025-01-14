from django.test import TestCase
from django.urls import reverse
from django.core.cache import cache
from AppFinVest.models import Usuario, TabelaGlobal
from django.contrib.auth.hashers import make_password


class TabelaViewsTest(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create(
            primeiro_nome="Gustavo",
            ultimo_nome="Silva",
            nome_usuario="gustavosilva",
            cpf= "12345678909",
            telefone= "11987654321",
            email="gustavo@example.com",
            senha=make_password("12345"),
            data_nascimento="2004-12-10"
        )

        # Simula dados de ações e criptomoedas
        self.tabela_global = TabelaGlobal.get_instance()
        self.tabela_global.acoes = [
            {"nome_ativo": "PETR4", "data": "2024-12-01", "abertura": 30.00, "maximo": 32.00, "minimo": 29.50, "fechamento": 31.50, "volume": 1000000},
        ]
        self.tabela_global.criptomoedas = [
            {"nome_ativo": "Bitcoin", "preco_atual": 50000.00, "capitalizacao_mercado": 900000000, "volume_24h": 50000000},
        ]

    def autenticar_usuario(self):
        """Simula o login do usuário armazenando o ID na sessão."""
        session = self.client.session
        session['usuario_id'] = self.usuario.id
        session.save()

    def test_tabela_acoes_view(self):
        self.autenticar_usuario()
        response = self.client.get(reverse('tabela_acoes'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PETR4")

    def test_tabela_acoes_mensagem_atualizacao(self):
        self.autenticar_usuario()
        cache.set("ação_atualizadas", ["PETR4"])
        response = self.client.get(reverse('tabela_acoes'))
        self.assertContains(response, "As seguintes ações foram atualizadas: PETR4")

    def test_criptomoedas_view(self):
        self.autenticar_usuario()
        response = self.client.get(reverse('criptomoedas'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Bitcoin")

    def test_criptomoedas_mensagem_atualizacao(self):
        self.autenticar_usuario()
        cache.set("criptomoeda_atualizadas", ["Bitcoin"])
        response = self.client.get(reverse('criptomoedas'))
        self.assertContains(response, "As seguintes criptomoedas foram atualizadas: Bitcoin")
