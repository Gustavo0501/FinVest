from django.views.generic import TemplateView
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils import timezone
import json
import calendar
import locale
from AppFinVest.models import Usuario, PerfilFinanceiro
from AppFinVest.decorators import login_required


class VisaoGeralView(TemplateView):
    template_name = 'AppFinVest/pages/visao-geral.html'

    @method_decorator(login_required)
    def get(self, request):
        usuario_id = request.session.get('usuario_id')
        usuario_logado = get_object_or_404(Usuario, id=usuario_id)

        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        now = timezone.now()
        mes_atual = calendar.month_name[now.month].capitalize()

        registro_usuario = PerfilFinanceiro.objects.filter(
            usuario=usuario_logado,
            mes_referente=mes_atual,
        )

        ultimo_registro = registro_usuario.first()
        
        if ultimo_registro:
            renda_atual = json.dumps(float(ultimo_registro.renda))
            divida_atual = json.dumps(float(ultimo_registro.divida))
            patrimonio_atual = json.dumps(float(ultimo_registro.patrimonio))
        else:
            renda_atual = json.dumps(0.0)
            divida_atual = json.dumps(0.0)
            patrimonio_atual = json.dumps(0.0)

        infos_financeiras = PerfilFinanceiro.objects.filter(usuario=usuario_logado).order_by('mes_referente')

        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

        dados_patrimonio = {mes: 0 for mes in meses}
        dados_renda = {mes: 0 for mes in meses}
        dados_divida = {mes: 0 for mes in meses}

        for info in infos_financeiras:
            dados_patrimonio[info.mes_referente] = float(info.patrimonio)
            dados_renda[info.mes_referente] = float(info.renda)
            dados_divida[info.mes_referente] = float(info.divida)

        
        patrimonio = [dados_patrimonio[mes] for mes in meses]
        renda = [dados_renda[mes] for mes in meses]
        dividas = [dados_divida[mes] for mes in meses]

        context = {
            "usuario": usuario_logado,
            "meses": json.dumps(meses),  # Serializando para JSON
            "patrimonio": json.dumps(patrimonio),
            "renda": json.dumps(renda),
            "dividas": json.dumps(dividas),
            "renda_atual": renda_atual,
            "divida_atual": divida_atual,
            "patrimonio_atual": patrimonio_atual,
        }

        return render(request, self.template_name, context)