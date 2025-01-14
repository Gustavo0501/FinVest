from django.test import TestCase, Client
from django.urls import reverse
from AppFinVest.models import Usuario, PerfilFinanceiro
from AppFinVest.formularios import FormularioRegistroUsuario, FormularioInfoFinanceiras

class RegistroUsuarioTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.registro_etapa1_url = reverse('registro')
        self.registro_etapa2_url = reverse('registroFinanceiro')

    # Teste do formulário de registro de usuário (Etapa 1)
    def test_formulario_registro_usuario_valido(self):
        form_data = {
            'primeiro_nome': 'Gustavo',
            'ultimo_nome': 'Silva',
            'nome_usuario': 'gustavosilva',
            'email': 'gustavo@example.com',
            'senha': 'senhaSegura123',
            'cpf': '12345678909',
            'telefone': '11987654321',
            'data_nascimento': '2004-12-10',
        }
        form = FormularioRegistroUsuario(data=form_data)
        self.assertTrue(form.is_valid())

    def test_formulario_registro_usuario_invalido(self):
        form_data = {
            'primeiro_nome': '',  # Nome vazio
            'ultimo_nome': 'Silva',
            'nome_usuario': 'gu',  # Nome de usuário muito curto
            'email': 'gustavo',  # E-mail inválido
            'senha': '123',  # Senha muito curta
            'cpf': '123',  # CPF inválido
            'telefone': '123',  # Telefone inválido
            'data_nascimento': '2025-01-01',
        }
        form = FormularioRegistroUsuario(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('primeiro_nome', form.errors)
        self.assertIn('nome_usuario', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('cpf', form.errors)
        self.assertIn('telefone', form.errors)

    # Teste de integração: fluxo de registro de usuário
    def test_registro_etapa1_view(self):
        response = self.client.post('/registro/', {
            'primeiro_nome': 'João',
            'ultimo_nome': 'Silva',
            'nome_usuario': 'joaosilva',
            'email': 'joao.silva@example.com',
            'senha': 'senhaSegura123',
            'cpf': '12345678909',
            'telefone': '31987654321',
            'data_nascimento': '2000-01-01',
        })
        self.assertEqual(response.status_code, 302)

    def test_registro_etapa2_view(self):
        session = self.client.session
        session['registro_dados'] = {
            'primeiro_nome': 'Gustavo',
            'ultimo_nome': 'Silva',
            'nome_usuario': 'gustavosilva',
            'email': 'gustavo@example.com',
            'senha': 'senhaSegura123',
            'cpf': '12345678901',
            'telefone': '11987654321',
            'data_nascimento': '2004-12-10',
        }
        session.save()

        response = self.client.post(self.registro_etapa2_url, {
            'renda': 5000.00,
            'divida': 1000.00,
            'patrimonio': 20000.00,
        })

        self.assertEqual(response.status_code, 302)
        usuario = Usuario.objects.get(email='gustavo@example.com')
        self.assertEqual(usuario.tipo_perfil, 'Investidor')

    def test_registro_etapa2_view_endividado(self):
        session = self.client.session
        session['registro_dados'] = {
            'primeiro_nome': 'Gustavo',
            'ultimo_nome': 'Silva',
            'nome_usuario': 'gustavosilva',
            'email': 'gustavo@example.com',
            'senha': 'senhaSegura123',
            'cpf': '12345678901',
            'telefone': '11987654321',
            'data_nascimento': '2004-12-10',
        }
        session.save()

        response = self.client.post(self.registro_etapa2_url, {
            'renda': 5000.00,
            'divida': 3000.00,
            'patrimonio': 10000.00,
        })

        self.assertEqual(response.status_code, 302)
        usuario = Usuario.objects.get(email='gustavo@example.com')
        self.assertEqual(usuario.tipo_perfil, 'Endividado')
