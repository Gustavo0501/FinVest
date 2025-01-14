from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from AppFinVest.formularios import FormularioRegistroUsuario


class RegistroEtapa1View(FormView):
    def get(self, request):
        form = FormularioRegistroUsuario()
        return render(request, 'registro_etapa1.html', {'form': form})

    def post(self, request):
        form = FormularioRegistroUsuario(request.POST)
        if form.is_valid():
            # Salvar o usuário e redirecionar para a próxima etapa
            form.save()
            return redirect('registroFinanceiro')
        return render(request, 'registro_etapa1.html', {'form': form})
