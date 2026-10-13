from django.db import models


class TrabalhoModel(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=150)
    descricao = models.TextField()
    orcamento = models.CharField(max_length=50)
    status = models.IntegerField(default=1)
    tipo = models.IntegerField()

    class Meta:
        db_table = "Trabalho"


class ServicoModel(models.Model):
    trabalho = models.OneToOneField(
        TrabalhoModel, primary_key=True, on_delete=models.CASCADE
    )
    metodologia = models.CharField(max_length=200)
    ferramenta = models.CharField(max_length=200)

    class Meta:
        db_table = "Servico"


class DemandaModel(models.Model):
    trabalho = models.OneToOneField(
        TrabalhoModel, primary_key=True, on_delete=models.CASCADE
    )
    exigencias = models.TextField()
    prazo = models.CharField(max_length=50)

    class Meta:
        db_table = "Demanda"


class PropostaModel(models.Model):
    id = models.AutoField(primary_key=True)
    orcamento = models.CharField(max_length=50)
    apresentacao = models.TextField()
    prazo = models.CharField(max_length=50)
    exigencia = models.TextField()
    tipo = models.IntegerField()
    status = models.IntegerField(default=1)
    

    class Meta:
        db_table = "Proposta"
