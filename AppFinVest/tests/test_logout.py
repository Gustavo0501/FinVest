from django.test import TestCase, Client
from django.urls import reverse
from AppFinVest.models import Usuario

class LogoutViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(
            primeiro_nome="Gustavo",
            ultimo_nome="Silva",
            nome_usuario="gustavosilva",
            cpf= "12345678909",
            telefone= "11987654321",
            email="gustavo@example.com",
            senha="12345",
            data_nascimento="2004-12-10"
        )
        self.client.session['usuario_id'] = self.usuario.id
        self.logout_url = reverse('logout')

    def test_logout_com_sessao_ativa(self):
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertNotIn('usuario_id', self.client.session)
