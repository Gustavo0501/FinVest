from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth.hashers import check_password

from AppFinVest.models import Usuario
from AppFinVest.formularios import FormularioLogin


class LoginView(FormView):
    template_name = 'AppFinVest/pages/login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('visao-geral')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        senha = form.cleaned_data['senha']
        try:
            usuario = Usuario.objects.get(email=email)
            if check_password(senha, usuario.senha):
                self.request.session['usuario_id'] = usuario.id
                return super().form_valid(form)
            else:
                form.add_error(None, "Senha incorreta.")
        except Usuario.DoesNotExist:
            form.add_error(None, "Usuário não encontrado.")
        return self.form_invalid(form)
