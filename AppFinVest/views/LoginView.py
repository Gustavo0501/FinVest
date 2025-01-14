from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
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
            if usuario.check_password(senha):
                # Login bem-sucedido
                self.request.session['usuario_id'] = usuario.id
                return redirect(self.success_url)
            else:
                form.add_error(None, "Senha incorreta.")
        except Usuario.DoesNotExist:
            form.add_error(None, "Usuário não encontrado.")

        return self.form_invalid(form)
