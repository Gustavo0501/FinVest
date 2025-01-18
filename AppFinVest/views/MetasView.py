from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from AppFinVest.decorators import login_required
from AppFinVest.models import MetaUsuario, Usuario

@method_decorator(login_required, name='dispatch')
class MetasView(TemplateView):
    template_name = 'AppFinVest/pages/metas.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Recupera o usuário logado ou da sessão
        usuario_id = self.request.session.get('usuario_id')
        usuario = Usuario.objects.get(id=usuario_id)

        # Recupera todas as metas do usuário
        metas = MetaUsuario.objects.filter(usuario=usuario)
        context['metas'] = metas
        context['usuario'] = usuario
        return context

    # Método para processar requisições POST (adicionar meta)
    def post(self, request, *args, **kwargs):
        usuario_id = self.request.session.get('usuario_id')
        usuario = Usuario.objects.get(id=usuario_id)

        # Criar uma nova meta com os dados enviados pelo formulário
        MetaUsuario.objects.create(
            usuario=usuario,
            nome_meta=request.POST['nome_meta'],
            valor_meta=request.POST['valor_meta'],
            data_meta=request.POST['data_meta']
        )

        # Redirecionar de volta para a página de metas
        return redirect('metas')