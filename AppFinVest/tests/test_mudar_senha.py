from django.test import TestCase
from django.urls import reverse
from AppFinVest.models import Usuario
from django.contrib.auth.hashers import make_password, check_password

class MudarSenhaViewTest(TestCase):
    def setUp(self):
        # Criando um usuário com senha criptografada
        self.usuario = Usuario.objects.create(
            primeiro_nome="Gustavo",
            ultimo_nome="Silva",
            nome_usuario="gustavosilva",
            cpf="12345678909",
            telefone="11987654321",
            email="gustavo@example.com",
            senha=make_password("senha_antiga"),
            data_nascimento="2004-12-10"
        )
        # Simulando a sessão de login
        session = self.client.session
        session['usuario_id'] = self.usuario.id
        session.save()

    def test_mudar_senha_com_dados_validos(self):
        dados = {
            'senha_antiga': 'senha_antiga',
            'nova_senha1': 'nova_senha123',
            'nova_senha2': 'nova_senha123'
        }
        response = self.client.post(reverse('mudar_senha'), dados)
        self.assertRedirects(response, reverse('perfil'))

        # Verificando se a senha foi alterada
        self.usuario.refresh_from_db()
        self.assertTrue(check_password('nova_senha123', self.usuario.senha))

    def test_mudar_senha_com_dados_invalidos(self):
        dados = {
            'senha_antiga': 'senha_errada',
            'nova_senha1': 'nova_senha123',
            'nova_senha2': 'nova_senha123'
        }
        response = self.client.post(reverse('mudar_senha'), dados)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Senha atual incorreta.')
