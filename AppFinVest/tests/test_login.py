from django.test import TestCase, Client
from django.urls import reverse
from AppFinVest.models import Usuario
from django.contrib.auth.hashers import make_password

class LoginViewTest(TestCase):

    def setUp(self):
        self.client = Client()
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
        self.login_url = reverse('login')

    def test_login_com_credenciais_validas(self):
        dados = {'email': 'gustavo@example.com', 'senha': '12345'}
        response = self.client.post(reverse('login'), dados)
        self.assertEqual(response.status_code, 302)  # Verifica redirecionamento
        self.assertRedirects(response, reverse('visao-geral'))

    def test_login_com_senha_incorreta(self):
        response = self.client.post(self.login_url, {'email': 'gustavo@example.com', 'senha': 'senhaerrada'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "A senha está incorreta.")

    def test_login_com_email_incorreto(self):
        response = self.client.post(self.login_url, {'email': 'naoencontrado@example.com', 'senha': '12345'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Nenhum usuário encontrado com este e-mail.")