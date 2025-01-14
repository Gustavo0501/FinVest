from django.test import TestCase, Client
from django.urls import reverse
from AppFinVest.models import Usuario
from django.contrib.auth.hashers import make_password

class PerfilViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.usuario = Usuario.objects.create(
            primeiro_nome="Gustavo",
            ultimo_nome="Silva",
            nome_usuario="gustavosilva",
            cpf="12345678909",
            telefone="11987654321",
            email="gustavo@example.com",
            senha=make_password("12345"),
            data_nascimento="2004-12-10"
        )
        # Configurando a sessão do usuário
        session = self.client.session
        session['usuario_id'] = self.usuario.id
        session.save()
        self.perfil_url = reverse('perfil')

    def test_visualizacao_perfil(self):
        response = self.client.get(self.perfil_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'AppFinVest/pages/perfil.html')

    def test_atualizacao_perfil(self):
        response = self.client.post(self.perfil_url, {
            'primeiro_nome': 'Gustavo',
            'ultimo_nome': 'Lima',
            'nome_usuario': 'gustavolima',
            'email': 'gustavo@example.com',
            'cpf': '12345678909',
            'telefone': '11987654321',
            'data_nascimento': '2004-12-10',
        })
        self.usuario.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.perfil_url)
        self.assertEqual(self.usuario.ultimo_nome, 'Lima')
        self.assertEqual(self.usuario.nome_usuario, 'gustavolima')
