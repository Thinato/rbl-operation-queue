from django.db import models

# Create your models here.
class Pedido(models.Model):
    codigo = models.CharField(verbose_name="Código", max_length=30)
    data_entrega = models.DateField(verbose_name="Data de Entrega")
    finalizado = models.BooleanField(verbose_name="Finalizado")

class Maquina(models.Model):
    nome = models.CharField(verbose_name="Nome", max_length=50)
    apelido = models.CharField(verbose_name="Apelido", max_length=50)
    custo_hora = models.FloatField(verbose_name="Custo/Hora", max_length=12)

class Peca(models.Model):
    cod_local = models.CharField(verbose_name="Código Local", max_length=50, primary_key=True)
    cod_estrangeiro = models.CharField(verbose_name="Código Estrangeiro", max_length=50)
    descricao = models.CharField(verbose_name="Descrição", max_length=200)
    
class Operacao(models.Model):
    peca = models.ForeignKey(Peca, to_field="cod_local", verbose_name="ID-Peça", on_delete=models.CASCADE)
    numero = models.IntegerField(verbose_name="Número")
    tempo_producao = models.IntegerField(verbose_name="Tempo Produção")
    tempo_ajuste = models.IntegerField(verbose_name="Tempo Ajuste")
    
class OperacaoMaquina(models.Model):
    maquina = models.ForeignKey(Maquina, verbose_name="ID-Máquina", on_delete=models.CASCADE)
    operacao = models.ForeignKey(Operacao, verbose_name="ID-Operação", on_delete=models.CASCADE)

class PedidoPeca(models.Model):
    pedido = models.ForeignKey(Pedido, verbose_name="ID-Pedido", on_delete=models.CASCADE)
    peca = models.ForeignKey(Peca, verbose_name="ID-Peça", on_delete=models.CASCADE)
    quantidade = models.IntegerField(verbose_name="Qtd.")

class FilaOperacao(models.Model):
    pedido = models.ForeignKey(Pedido, verbose_name="ID-Pedido", on_delete=models.CASCADE)
    maquina = models.ForeignKey(Maquina, verbose_name="ID-Maquina", on_delete=models.CASCADE)
    operacao = models.ForeignKey(Operacao, verbose_name="ID-Operação", on_delete=models.CASCADE)
    quantidade_feita = models.IntegerField(verbose_name="Qtd. Feita")
    peso = models.IntegerField(verbose_name="Peso")