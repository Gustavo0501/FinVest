from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
from django.core.cache import cache

from AppFinVest.decorators import login_required
from AppFinVest.models import TabelaGlobal


class TabelaAcoesView(View):
    template_name = 'AppFinVest/pages/acoes.html'

    @method_decorator(login_required)
    def get(self, request):
        tabela_global = TabelaGlobal.get_instance()
        dados_acoes = [
            {
                "nome_ativo": acao.nome_ativo,
                "data": acao.data,
                "abertura": acao.abertura,
                "maximo": acao.maximo,
                "minimo": acao.minimo,
                "fechamento": acao.fechamento,
                "volume": acao.volume,
            }
            for acao in tabela_global.get_acoes()
        ]

        acoes_atualizadas = cache.get("ação_atualizadas", [])
        mensagem_atualizacao = f"As seguintes ações foram atualizadas: {', '.join(acoes_atualizadas)}" if acoes_atualizadas else None

        # Limpa a cache após exibir a mensagem
        cache.delete("ação_atualizadas")

        return render(request, self.template_name, {'dados_acoes': dados_acoes, 'mensagem_atualizacao': mensagem_atualizacao})
