from django.views import View
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from AppFinVest.decorators import login_required


class LogoutView(View):
    
    @method_decorator(login_required)
    def post(self, request):
        if 'usuario_id' in request.session:
            del request.session['usuario_id']
        return redirect('login')
