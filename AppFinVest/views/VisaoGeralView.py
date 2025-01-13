from django.views.generic import TemplateView
from django.utils.decorators import method_decorator

from AppFinVest.decorators import login_required


@method_decorator(login_required, name='dispatch')
class VisaoGeralView(TemplateView):
    template_name = 'AppFinVest/pages/visao-geral.html'
