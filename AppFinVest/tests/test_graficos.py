from django.test import TestCase
from django.urls import reverse
from AppFinVest.models import Usuario, PerfilFinanceiro
from django.utils.timezone import now
import calendar
from django.contrib.auth.hashers import make_password

class GraficosViewTest(TestCase):
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

    def autenticar_usuario(self):
        """Simula o login do usuário armazenando o ID na sessão."""
        session = self.client.session
        session['usuario_id'] = self.usuario.id
        session.save()

    def test_exibir_graficos_com_dados_financeiros(self):
        self.autenticar_usuario()  # Simula o login
        response = self.client.get(reverse('graficos'))
        self.assertEqual(response.status_code, 200)

    def test_atualizar_dados_financeiros(self):
        self.autenticar_usuario()  # Simula o login
        data = {
            'renda': 7000,
            'divida': 3000,
            'patrimonio': 15000,
        }
        response = self.client.post(reverse('graficos'), data)
        self.assertEqual(response.status_code, 200)

        # Verifica se os dados foram atualizados corretamente
        registro = PerfilFinanceiro.objects.get(usuario=self.usuario, mes_referente="Janeiro")
        self.assertEqual(registro.renda, 7000)
        self.assertEqual(registro.divida, 3000)
        self.assertEqual(registro.patrimonio, 15000)
