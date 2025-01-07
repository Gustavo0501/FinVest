from django.db import models

class Usuario(models.Model):
    primeiro_nome = models.CharField(max_length=45)
    ultimo_nome = models.CharField(max_length=45)
    nome_usuario = models.CharField(max_length=45, unique=True)
    cpf = models.CharField(max_length=11, unique=True) # apenas os números
    telefone = models.CharField(max_length=11) # apenas os números
    data_nascimento = models.DateField()
    #foto_perfil = models.ImageField(
    #    upload_to='recipes/covers/%Y/%m/%d/', blank=True, default='')
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




