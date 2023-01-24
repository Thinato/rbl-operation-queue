from django import forms

class NovaPeca(forms.Form):
    codigo_local = forms.CharField(label='Cód. Estrangeiro', max_length=50)
    codigo_estrangeiro = forms.CharField(label='Cód. Estrangeiro', max_length=50)
    qtd_operacoes = forms.IntegerField(label="Qtd. de Operações", min_value=1, max_value=16)
    descricao = forms.CharField(label='Descrição', max_length=200, required=False)

class EditarPeca(forms.Form):
    codigo_estrangeiro = forms.CharField(label='Cód. Estrangeiro', max_length=50)
    qtd_operacoes = forms.IntegerField(label="Qtd. de Operações", min_value=1, max_value=16)
    descricao = forms.CharField(label='Descrição', max_length=200, required=False)

class NovaOperacao(forms.Form):
    tempo_operacao = forms.IntegerField(label='Tempo de Operação')
    tempo_ajuste = forms.IntegerField(label='Tempo de Ajuste')

class NovaMaquina(forms.Form):
    nome = forms.CharField(label='Nome', max_length=50, required=True)
    apelido = forms.CharField(label='Apelido', max_length=50, required=False)
    custo_hora = forms.FloatField(label='Custo/Hora', required=False)

class NovoPedido(forms.Form):
    codigo = forms.CharField(
        label='Código', 
        max_length=50, 
        required=True
        )
    data_entrega = forms.DateField(
        label='Data de Entrega',
        input_formats=['%d/%m/%Y'], 
        required=True,
        widget=forms.DateInput(attrs={
            'placeholder': 'dia/mês/ano'
            })
    )
    
class NovoItem(forms.Form):
    codigo_local = forms.CharField(label='Código', max_length=50, required=True)
    quantidade = forms.IntegerField(label='Quantidade', required=True)
