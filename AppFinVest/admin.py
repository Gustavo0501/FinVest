from django.contrib import admin
from .models import Usuario, PerfilFinanceiro, Observer, PrecoAtivo, TabelaGlobal

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    ...


@admin.register(PerfilFinanceiro)
class PerfilFinanceiroAdmin(admin.ModelAdmin):
    ...


@admin.register(Observer)
class ObserverAdmin(admin.ModelAdmin):
    ...


@admin.register(PrecoAtivo)
class PrecoAtivoAdmin(admin.ModelAdmin):
    ...


@admin.register(TabelaGlobal)
class TabelaGlobalAdmin(admin.ModelAdmin):
    ...




