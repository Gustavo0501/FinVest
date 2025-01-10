from django.db import models
from django.utils.translation import gettext_lazy as _

class Usuario(models.Model):
    primeiro_nome = models.CharField(max_length=45)
    ultimo_nome = models.CharField(max_length=45)
    nome_usuario = models.CharField(max_length=45, unique=True)
    cpf = models.CharField(max_length=11, unique=True) # apenas os números
    telefone = models.CharField(max_length=11) # apenas os números
    data_nascimento = models.DateField()
    email = models.EmailField(_("email"))
    senha = models.CharField(_("senha"), max_length=128)
    tipo_perfil = models.CharField(max_length=45)

    def __str__(self):
        return self.nome_usuario


class PerfilFinanceiro(models.Model):
    tipo_perfil = models.CharField(max_length=45)
    renda = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    divida = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    patrimonio = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    mes_referente = models.CharField(max_length=7, null=False)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="usuario")

    def __str__(self):
        return f"Perfil: {self.tipo_perfil} Renda: {self.renda}, Dívida: {self.divida}, Patrimônio: {self.patrimonio} Mês referente: {self.mes_referente}"




class PrecoAtivo(models.Model):
    nome_ativo = models.CharField(max_length=100)  # Ação e Criptomoeda
    tipo = models.CharField(max_length=50, choices=[("Ação", "Ação"), ("Criptomoeda", "Criptomoeda")]) # Este atributo não será atualizado
    preco_atual = models.FloatField(default=0.0, null=True, blank=True) # Criptomoeda
    capitalizacao_mercado = models.FloatField(null=True, blank=True) # Criptomoeda
    volume_24h = models.FloatField(null=True, blank=True) # Criptomoeda
    data = models.DateField() # Ação
    abertura = models.FloatField(null=True, blank=True) # Ação
    maximo = models.FloatField(null=True, blank=True) # Ação
    minimo = models.FloatField(null=True, blank=True) # Ação
    fechamento = models.FloatField(null=True, blank=True) # Ação
    volume = models.BigIntegerField(null=True, blank=True) # Ação          

    def atualizar_ativo_acao(self, data=None, abertura=None, maximo=None, minimo=None, fechamento=None, volume=None):
        self.data = data
        self.abertura = abertura
        self.maximo = maximo
        self.minimo = minimo
        self.fechamento = fechamento
        self.volume = volume
        self.save()
        print(f"Ação {self.nome_ativo} atualizada com sucesso.")

    # 🔧 Método para atualizar criptomoedas
    def atualizar_ativo_criptomoeda(self, preco_atual=None, capitalizacao_mercado=None, volume_24h=None):
        self.preco_atual = preco_atual
        self.capitalizacao_mercado = capitalizacao_mercado
        self.volume_24h = volume_24h
        self.save()
        print(f"Criptomoeda {self.nome_ativo} atualizada com sucesso.")

    def adicionar_observer(self, observer):
        Observer.objects.create(ativo=self, **observer)

    def remover_observer(self, observer):
        Observer.objects.filter(ativo=self, **observer).delete()

    def notificar_observers(self):
        for observer in self.observers.all():
            observer.atualizar(self.preco_atual)

    def __str__(self):
        return f"{self.nome_ativo} ({self.tipo}): R$ {self.preco_atual}"

class Observer(models.Model):
    ativo = models.ForeignKey(PrecoAtivo, on_delete=models.CASCADE, related_name="observers")

    def atualizar(self, preco):
        # Implemente a lógica de notificação desejada
        print(f"O preço do ativo foi atualizado para {preco:.2f}")

    def adicionar_observer(self, observer_instance):
        Observer.objects.create(ativo=self)

    def remover_observer(self, observer_instance):
        Observer.objects.filter(ativo=self).delete()

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

