from django.db import models
from django.contrib.auth.hashers import check_password, make_password
from django.utils.translation import gettext_lazy as _
from django.contrib.messages import add_message
from django.contrib.messages.constants import INFO
from django.core.cache import cache

class Usuario(models.Model):
    primeiro_nome = models.CharField(max_length=45)
    ultimo_nome = models.CharField(max_length=45)
    nome_usuario = models.CharField(max_length=45, unique=True)
    cpf = models.CharField(max_length=11, unique=True) # apenas os números
    telefone = models.CharField(max_length=11) # apenas os números
    data_nascimento = models.DateField()
    email = models.EmailField(_("email"), unique=True)
    senha = models.CharField(_("senha"), max_length=128)
    tipo_perfil = models.CharField(max_length=45)

    def __str__(self):
        return self.nome_usuario

    def set_password(self, raw_password):
        self.senha = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        return check_password(raw_password, self.senha)


class PerfilFinanceiro(models.Model):
    tipo_perfil = models.CharField(max_length=45)
    renda = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    divida = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    patrimonio = models.DecimalField(max_digits=15, decimal_places=2, null=False)
    mes_referente = models.CharField(max_length=7, null=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuario")

    def __str__(self):
        return f"Perfil: {self.tipo_perfil} Renda: {self.renda}, Dívida: {self.divida}, Patrimônio: {self.patrimonio} Mês referente: {self.mes_referente}"



class PrecoAtivo(models.Model):
    nome_ativo = models.CharField(max_length=100)  # Nome do ativo (Ação ou Criptomoeda)
    tipo = models.CharField(
        max_length=50,
        choices=[("Ação", "Ação"), ("Criptomoeda", "Criptomoeda")],
    )  # Tipo do ativo
    preco_atual = models.FloatField(default=0.0, null=True, blank=True)  # Criptomoeda
    capitalizacao_mercado = models.FloatField(null=True, blank=True)  # Criptomoeda
    volume_24h = models.FloatField(null=True, blank=True)  # Criptomoeda
    data = models.DateField(null=True, blank=True)  # Ação
    abertura = models.FloatField(null=True, blank=True)  # Ação
    maximo = models.FloatField(null=True, blank=True)  # Ação
    minimo = models.FloatField(null=True, blank=True)  # Ação
    fechamento = models.FloatField(null=True, blank=True)  # Ação
    volume = models.BigIntegerField(null=True, blank=True)  # Ação


    def save(self, *args, **kwargs):
        """Salva o ativo e garante que um observer padrão exista."""
        super().save(*args, **kwargs)
        if not self.observers.exists():
            Observer.objects.create(ativo=self)  # Cria um observer padrão

    # Método para atualizar dados de ações
    def atualizar_ativo_acao(self, data=None, abertura=None, maximo=None, minimo=None, fechamento=None, volume=None, request=None):
        self.data = data
        self.abertura = abertura
        self.maximo = maximo
        self.minimo = minimo
        self.fechamento = fechamento
        self.volume = volume
        self.save()
        print(f"Ação {self.nome_ativo} atualizada com sucesso.")
        self.notificar_observers(request)

    # Método para atualizar dados de criptomoedas
    def atualizar_ativo_criptomoeda(self, preco_atual=None, capitalizacao_mercado=None, volume_24h=None, request=None):
        self.preco_atual = preco_atual
        self.capitalizacao_mercado = capitalizacao_mercado
        self.volume_24h = volume_24h
        self.save()
        print(f"Criptomoeda {self.nome_ativo} atualizada com sucesso.")
        self.notificar_observers(request)

    # Método para adicionar um observer
    def adicionar_observer(self, observer):
        Observer.objects.create(ativo=self, **observer)

    # Método para remover um observer
    def remover_observer(self, observer):
        Observer.objects.filter(ativo=self, **observer).delete()

    # Método para notificar os observers
    def notificar_observers(self, request=None):
        for observer in self.observers.all():
            observer.atualizar(self, request)

    def __str__(self):
        return f"{self.nome_ativo} ({self.tipo}): R$ {self.preco_atual}"



class Observer(models.Model):
    ativo = models.ForeignKey("PrecoAtivo", on_delete=models.CASCADE, related_name="observers")

    def atualizar(self, ativo, request=None):
        tipo = ativo.tipo.lower()  # "ação" ou "criptomoeda"
        cache_key = f"{tipo}_atualizadas"  # "ação_atualizadas" ou "criptomoeda_atualizadas"

        # Recupera a lista atual do cache
        ativos_atualizados = cache.get(cache_key, [])
        if ativo.nome_ativo not in ativos_atualizados:
            ativos_atualizados.append(ativo.nome_ativo)
        cache.set(cache_key, ativos_atualizados, timeout=3600)  # Expira em 1 hora


    def __str__(self):
        return f"Observador do ativo {self.ativo.nome_ativo}"



# Singleton para armazenar os ativos globalmente
class TabelaGlobal(models.Model):
    ativos = models.ManyToManyField(PrecoAtivo)

    @classmethod
    def get_instance(cls):
        instance, _ = cls.objects.get_or_create(pk=1)
        return instance

    # Método para retornar apenas as ações
    def get_acoes(self):
        return self.ativos.filter(tipo="Ação")

    # Método para retornar apenas as criptomoedas
    def get_criptomoedas(self):
        return self.ativos.filter(tipo="Criptomoeda")


class MetaUsuario(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="metas")
    nome_meta = models.CharField(max_length=100)
    valor_meta = models.DecimalField(max_digits=15, decimal_places=2)
    data_meta = models.DateField()
    atingida = models.BooleanField(default=False)
    valor_atual = models.DecimalField(max_digits=15, decimal_places=2, default=0.0)
    automatica = models.BooleanField(default=False)

    def __str__(self):
        return f"Meta: {self.nome_meta} - Valor: R$ {self.valor_meta}"


