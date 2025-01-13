from django.views import View
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator

from django.http import JsonResponse
from AppFinVest.decorators import login_required
from AppFinVest.models import Usuario
from AppFinVest.formularios import FormularioPerfilUsuario



class PerfilView(View):
    template_name = 'AppFinVest/pages/perfil.html'

    @method_decorator(login_required)
    def get(self, request):
        usuario_id = request.session.get('usuario_id')
        usuario_logado = get_object_or_404(Usuario, id=usuario_id)
        form = FormularioPerfilUsuario(instance=usuario_logado)
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        usuario_id = request.session.get('usuario_id')
        usuario_logado = get_object_or_404(Usuario, id=usuario_id)
        form = FormularioPerfilUsuario(request.POST, instance=usuario_logado)
        if form.is_valid():
            form.save()
            return redirect('perfil')
        return render(request, self.template_name, {'form': form})
