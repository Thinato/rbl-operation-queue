from django import template
from main.models import Operacao, Peca, PedidoPeca, Operacao, Maquina, OperacaoMaquina
from django.db.models import Q

register = template.Library()

@register.filter
def keyvalue(dict, key):    
    return dict[key]

@register.filter
def sortbyname(data_set):    
    return sorted(data_set, key=lambda x: x.nome)

@register.filter
def orderby_data_entrega(data_set):    
    return sorted(data_set, key=lambda x: x.data_entrega)

@register.filter
def get_values(fila, maq):
    return fila[maq]

@register.filter
def get_op(fop):
    return Operacao.objects.get(id=fop.operacao.id)

@register.filter
def get_peca(op):
    return op.peca.cod_local

@register.filter
def upper(text: str):    
    return text.upper()

@register.filter
def mult(n1, n2):    
    return n1*n2

@register.filter
def over(n1, n2):    
    return n1/n2

@register.filter
def over_floor(n1, n2):    
    return n1//n2

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def length(x):
    return len(x)

@register.filter
def fila_col(fila):
    return 12//len(fila)

@register.filter
def get_quantidade(fop):
    pp = PedidoPeca.objects.get(Q(peca=fop.operacao.peca.cod_local) & Q(pedido=fop.pedido))
    return pp.quantidade

@register.filter
def get_maquinas(op):
    return [op_maq.maquina for op_maq in OperacaoMaquina.objects.filter(operacao=op)]

# @register.filter
# def op_numero(fop):
#     return fop.operacao

