from django.shortcuts import redirect

def registro_required(view_func):
    """
    Verifica se os dados de registro estão na sessão. Caso contrário, redireciona para a página de registro.
    """
    def wrapper(request, *args, **kwargs):
        if 'registro_dados' not in request.session:
            return redirect('registro')
        return view_func(request, *args, **kwargs)
    return wrapper

def login_required(view_func):
    """
    Verifica se o usuário está autenticado. Caso contrário, redireciona para a página de login.
    """
    def wrapper(request, *args, **kwargs):
        if 'usuario_id' not in request.session:
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper
