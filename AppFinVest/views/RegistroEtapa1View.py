from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from AppFinVest.formularios import FormularioRegistroUsuario


class RegistroEtapa1View(FormView):
    def get(self, request):
        form = FormularioRegistroUsuario()
        return render(request, 'AppFinVest/pages/registro_etapa1.html', {'form': form})

    def post(self, request):
        form = FormularioRegistroUsuario(request.POST)
        if form.is_valid():
            # Armazenar os dados do usuário na sessão
            dados_usuario = form.cleaned_data
            dados_usuario['data_nascimento'] = dados_usuario['data_nascimento'].strftime('%Y-%m-%d')  # Converter para string
            request.session['registro_dados'] = dados_usuario

            return redirect('registroFinanceiro')
        return render(request, 'AppFinVest/pages/registro_etapa1.html', {'form': form})
