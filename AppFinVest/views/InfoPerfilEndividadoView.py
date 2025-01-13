from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from AppFinVest.decorators import registro_required


@method_decorator(registro_required, name='dispatch')
class InfoPerfilEndividadoView(TemplateView):
    template_name = 'AppFinVest/pages/perfilEndividado.html'
