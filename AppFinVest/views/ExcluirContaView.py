from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import redirect

from AppFinVest.decorators import login_required
from AppFinVest.models import Usuario


class ExcluirContaView(View):
    @method_decorator(login_required)
    def post(self, request):
        usuario_id = request.session.get('usuario_id')
        try:
            usuario = Usuario.objects.get(id=usuario_id)
            usuario.delete()
            request.session.flush()
            return redirect('login')
        except Usuario.DoesNotExist:
            return redirect('perfil')

    @method_decorator(login_required)
    def get(self, request):
        return redirect('perfil')
