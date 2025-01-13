from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from AppFinVest.formularios import FormularioRegistroUsuario


class RegistroEtapa1View(FormView):
    template_name = 'AppFinVest/pages/registro_etapa1.html'
    form_class = FormularioRegistroUsuario
    success_url = reverse_lazy('registroFinanceiro')

    def form_valid(self, form):
        dados_pessoais = form.cleaned_data
        dados_pessoais['data_nascimento'] = str(dados_pessoais['data_nascimento'])
        self.request.session['registro_dados'] = dados_pessoais
        return super().form_valid(form)
