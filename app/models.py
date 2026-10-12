from django.db import models


# Define o Model de Trabalho
class TrabalhoModel(models.Model):
    # define os campos
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    orcamento = models.CharField(max_length=50)
    status = models.IntegerField(default=1)

    class Meta:
        # define o nome da tabela
        db_table = "Trabalho"


# Define o Model de Serviço (o id é o mesmo id do Trabalho)
class ServicoModel(models.Model):
    # define os campos
    trabalho = models.OneToOneField(
        TrabalhoModel, primary_key=True, on_delete=models.CASCADE
    )
    metodologia = models.CharField(max_length=200)
    ferramenta = models.CharField(max_length=200)

    class Meta:
        # define o nome da tabela
        db_table = "Servico"


# Define o Model de Demanda (o id é o mesmo id do Trabalho)
class DemandaModel(models.Model):
    # define os campos
    trabalho = models.OneToOneField(
        TrabalhoModel, primary_key=True, on_delete=models.CASCADE
    )
    exigencias = models.TextField()
    prazo = models.CharField(max_length=50)

    class Meta:
        # define o nome da tabela
        db_table = "Demanda"


# Define o Model de Proposta
class PropostaModel(models.Model):
    # define os campos
    id = models.AutoField(primary_key=True)
    orcamento = models.CharField(max_length=50)
    apresentacao = models.TextField()
    prazo = models.CharField(max_length=50)
    exigencia = models.TextField()
    tipo = models.IntegerField()
    status = models.IntegerField(default=1)

    class Meta:
        # define o nome da tabela
        db_table = "Proposta"
