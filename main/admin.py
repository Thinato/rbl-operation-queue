from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Pedido)
admin.site.register(Maquina)
admin.site.register(Peca)
admin.site.register(Operacao)
admin.site.register(OperacaoMaquina)
admin.site.register(PedidoPeca)