from django.views import View
from django.shortcuts import render, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils import timezone
import json
import calendar
import locale
from AppFinVest.models import Usuario, PerfilFinanceiro
from AppFinVest.decorators import login_required


class GraficosView(View):
    template_name = 'AppFinVest/pages/graficos.html'

    @method_decorator(login_required)
    def get(self, request):
        """
        Processa a requisição GET para exibir os dados do usuário e gráficos.
        """
        # Pegando o usuário logado
        usuario_id = request.session.get('usuario_id')
        usuario_logado = get_object_or_404(Usuario, id=usuario_id)

        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

        # Obtém o mês e o ano atuais
        now = timezone.now()
        mes_atual = calendar.month_name[now.month].capitalize()

        # Filtra os registros financeiros do usuário logado para o mês atual
        registro_usuario = PerfilFinanceiro.objects.filter(
            usuario=usuario_logado,
            mes_referente=mes_atual,
        )

        # Obtém o último registro, se existir
        ultimo_registro = registro_usuario.first()

        if ultimo_registro:
            renda_atual = json.dumps(float(ultimo_registro.renda))
            divida_atual = json.dumps(float(ultimo_registro.divida))
            patrimonio_atual = json.dumps(float(ultimo_registro.patrimonio))
        else:
            renda_atual = json.dumps(0.0)
            divida_atual = json.dumps(0.0)
            patrimonio_atual = json.dumps(0.0)

        #=====================================================================
        # Filtrando as informações financeiras do usuário logado
        infos_financeiras = PerfilFinanceiro.objects.filter(usuario=usuario_logado).order_by('mes_referente')

        # Lista de meses em ordem
        meses = [
            "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
            "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
        ]

        # Inicializando dicionários para armazenar os dados agrupados por mês
        dados_patrimonio = {mes: [] for mes in meses}
        dados_renda = {mes: [] for mes in meses}
        dados_divida = {mes: [] for mes in meses}

        # Preenchendo os dicionários com os valores financeiros
        for info in infos_financeiras:
            dados_patrimonio[info.mes_referente] = float(info.patrimonio)
            dados_renda[info.mes_referente] = float(info.renda)
            dados_divida[info.mes_referente] = float(info.divida)

        # Transformando os dicionários em listas que o gráfico possa entender
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

    @method_decorator(login_required)
    def post(self, request):
        """
        Processa a requisição POST para atualizar os dados financeiros do usuário.
        """
        # Pegando o usuário logado
        usuario_id = request.session.get('usuario_id')
        usuario_logado = get_object_or_404(Usuario, id=usuario_id)

        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

        # Obtém o mês e o ano atuais
        now = timezone.now()
        mes_atual = calendar.month_name[now.month].capitalize()

        # Filtra os registros financeiros do usuário logado para o mês atual
        registro_usuario = PerfilFinanceiro.objects.filter(
            usuario=usuario_logado,
            mes_referente=mes_atual,
        ).first()

        # Atualiza ou cria o registro
        renda = request.POST.get('renda')
        divida = request.POST.get('divida')
        patrimonio = request.POST.get('patrimonio')

        if registro_usuario:
            registro_usuario.renda = renda
            registro_usuario.divida = divida
            registro_usuario.patrimonio = patrimonio
            registro_usuario.save()
        else:
            PerfilFinanceiro.objects.create(
                usuario=usuario_logado,
                tipo_perfil=usuario_logado.tipo_perfil,
                mes_referente=mes_atual,
                renda=renda,
                divida=divida,
                patrimonio=patrimonio,
            )

        return self.get(request)
