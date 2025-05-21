from django.db import models
from datetime import date

# Principal model: Socio
class Socio(models.Model):
    STATUS_CHOICES = [
        ('Ativo', 'Ativo'),
        ('Inativo', 'Inativo'),
        ('Suspenso', 'Suspenso'),
    ]

    matricula = models.CharField(max_length=10, unique=True, null=True)
    nome = models.CharField(max_length=255, blank=False)
    data_nasc = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=14, unique=True, null=True)
    rg = models.CharField(max_length=20, unique=True, blank=True)
    telefone = models.CharField(max_length=20, null=True, blank=True)
    data_socio = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ativo')
    documento_vencimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.nome} (Matrícula: {self.matricula})'

    def is_document_expiring_soon(self):
        """Check if a document is expiring within the next 30 days."""
        if self.documento_vencimento:
            return (self.documento_vencimento - date.today()).days <= 30
        return False


# Lotação / Local de trabalho
class Lotacao(models.Model):
    socio_lotacao = models.CharField(max_length=255, null=True, blank=True)  # Ex: Prefeitura, Câmara, etc
    secretaria = models.CharField(max_length=255, null=True, blank=True)  # Ex: Secretaria de Educação
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='lotacoes')

    def __str__(self):
        return f"{self.socio.nome} - Lotação: {self.socio_lotacao or ''} - {self.secretaria or ''}"


# Cargo e data de admissão do sócio
class SocioTrabalho(models.Model):
    data_admissao = models.DateField(null=True, blank=True)
    cargo = models.CharField(max_length=255, null=True, blank=True)
    lotacao = models.ForeignKey(Lotacao, on_delete=models.SET_NULL, null=True, blank=True, related_name='trabalhos')
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='trabalhos')

    def __str__(self):
        return f"{self.socio.nome} - {self.cargo or 'Sem cargo'}"


# Endereço do sócio
class SocioEndereco(models.Model):
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='enderecos')
    rua = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=20, null=True, blank=True)
    bairro = models.CharField(max_length=255, null=True, blank=True)
    cidade = models.CharField(max_length=255, null=True, blank=True)
    cep = models.CharField(max_length=10, null=True, blank=True)
    uf = models.CharField(max_length=2, null=True, blank=True)

    def __str__(self):
        return f"{self.socio.nome} - {self.bairro or 'Não informado'}"


# Dependentes do sócio
class SocioDependent(models.Model):
    nome = models.CharField(max_length=255, null=True, blank=True)
    socio = models.ForeignKey(Socio, on_delete=models.CASCADE, related_name='dependentes')

    def __str__(self):
        return f"{self.nome} (Dependente de {self.socio.nome})"
