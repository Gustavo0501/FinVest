from .models import Usuario

def usuario_logado(request):
    if request.session.get('usuario_id'):
        try:
            usuario = Usuario.objects.get(id=request.session['usuario_id'])
            return {'usuario_logado': usuario}
        except Usuario.DoesNotExist:
            return {}
    return {}