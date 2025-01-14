from django.shortcuts import redirect
from functools import wraps
from django.shortcuts import render, get_object_or_404
from AppFinVest.models import Usuario

def registro_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('registro_dados'):
            return redirect('registro')  # Redireciona para a etapa 1 do registro
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def login_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        usuario_id = request.session.get('usuario_id')
        try:
            # Tenta buscar o usuário no banco de dados
            usuario_logado = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            # Se o usuário não for encontrado, redireciona para a página de login
            return redirect('login')

        # Continua para a view original
        return view_func(request, *args, **kwargs)
    return _wrapped_view