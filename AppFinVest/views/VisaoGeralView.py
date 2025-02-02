from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from AppFinVest.decorators import login_required
from AppFinVest.models import Usuario


@method_decorator(login_required, name='dispatch')
class VisaoGeralView(TemplateView):
    template_name = 'AppFinVest/pages/visao-geral.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Pegue o usuário personalizado (ajuste de acordo com sua lógica)
        # Exemplo: Suponha que você armazena o ID do usuário logado na sessão
        usuario_id = self.request.session.get('usuario_id')
        if not usuario_id:
            raise ValueError("Usuário não encontrado na sessão.")

        # Recupere o usuário personalizado pelo ID (ou outro identificador)
        usuario = Usuario.objects.get(id=usuario_id)
        context['usuario'] = usuario

        return context
