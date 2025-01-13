from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.decorators import method_decorator

from AppFinVest.decorators import login_required
from AppFinVest.models import Usuario
from AppFinVest.formularios import FormularioMudarSenha


class MudarSenhaView(View):
    template_name = 'AppFinVest/pages/mudar_senha.html'

    @method_decorator(login_required)
    def get(self, request):
        usuario_id = request.session.get('usuario_id')
        usuario_logado = get_object_or_404(Usuario, id=usuario_id)
        form = FormularioMudarSenha(Usuario=usuario_logado)
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        usuario_id = request.session.get('usuario_id')
        usuario_logado = get_object_or_404(Usuario, id=usuario_id)
        form = FormularioMudarSenha(request.POST, Usuario=usuario_logado)
        if form.is_valid():
            form.save()
            return redirect('perfil')
        return render(request, self.template_name, {'form': form})
