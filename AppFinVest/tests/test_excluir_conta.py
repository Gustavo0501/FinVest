from django.test import TestCase, Client
from django.urls import reverse
from AppFinVest.models import Usuario

class ExcluirContaViewTest(TestCase):

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
        self.excluir_conta_url = reverse('excluir_conta')

    def test_excluir_conta_com_usuario_valido(self):
        response = self.client.post(self.excluir_conta_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(not Usuario.objects.filter(id=self.usuario.id).exists())