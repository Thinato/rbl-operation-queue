from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Q
from .forms import *
from .models import *
import datetime
from time import sleep


# Create your views here.
def base(request):
    return render(request, 'main/base.html')

def registro(request):
    maquinas = Maquina.objects.all()
    pecas = Peca.objects.all()
    return render(request, 'main/registro.html', {'maquinas':maquinas, 'pecas':pecas})

def search(request):
    if request.method == 'GET':
        searched = request.GET['search']
        pecas = Peca.objects.filter(Q(cod_local__contains=searched) | Q(cod_estrangeiro__contains=searched))

        return render(request, 'main/search.html', {'searched':searched, 'pecas':pecas})

def instancia(request):
    
    fila = {}
    status = {}
    previsao = {}
    edicao = False
    if request.method == "POST":
        if request.POST.get('add_peso'):
            fop = FilaOperacao.objects.get(id=request.POST.get('add_peso'))
            shift = FilaOperacao.objects.get(Q(maquina=fop.maquina) & Q(peso=fop.peso + 1))
            shift.peso -= 1
            fop.peso += 1
            shift.save()
            fop.save()
        elif request.POST.get('sub_peso'):
            fop = FilaOperacao.objects.get(id=request.POST.get('sub_peso'))
            shift = FilaOperacao.objects.get(Q(maquina=fop.maquina) & Q(peso=fop.peso - 1))
            shift.peso += 1
            fop.peso -= 1
            shift.save()
            fop.save()
        elif request.POST.get('ok'):
            fop = FilaOperacao.objects.get(id=request.POST.get('ok'))
            maq = Maquina.objects.get(id=request.POST.get('maquina'))
            for i in FilaOperacao.objects.filter(Q(peso__gte=fop.peso) & Q(maquina=fop.maquina)):
                i.peso -= 1
                i.save()

            fop.maquina = maq
            fop.peso = FilaOperacao.objects.filter(maquina=maq).count()
            fop.save()



    for maq in Maquina.objects.all():
        if request.GET.get('edicao'):
            edicao = True
        if request.GET.get(f'maq_{maq.id}'):
            fila[maq] = []

        for op in FilaOperacao.objects.all():
            if op.maquina == maq and op.peso >= 0:# and op.quantidade_feita < PedidoPeca.objects.get(Q(pedido=op.pedido) & Q(peca=op.operacao.peca)).quantidade:
                fila[maq].append(op)

            
    for maq in fila.keys():
        fila[maq] = sorted(fila[maq], key=lambda x: x.peso)
    
    for maq in fila.keys():
        for fop in fila[maq]:
            if fop not in status:
                if fop.peso == 0:
                    status[fop] = 'active'
                else:
                    status[fop] = 'inactive'

            for c_maq in fila.keys():
                for c_fop in fila[c_maq]:
                    if c_fop != fop:
                        if c_fop.pedido == fop.pedido and c_fop.operacao.peca == fop.operacao.peca and fop.operacao.numero > c_fop.operacao.numero:
                            if fop.peso < c_fop.peso or fop.peso == 0 and c_fop.peso == 0:
                                status[fop] = 'error'
                                status[c_fop] = 'error'
                            elif fop.peso == c_fop.peso:
                                status[fop] = 'warning'

            
            

    
        
    return render(request, 'main/instancia.html', {'fila':fila, 'edicao':edicao, 'status':status, 'previsao':previsao})

def nova_maquina(request, index=None):
    if request.method == 'POST':
        if request.POST.get('salvar'):
            custo = 0
            if request.POST.get('custo_hora'):
                custo = float(request.POST.get('custo_hora'))
            maq = Maquina(
                nome=request.POST.get('nome'),
                apelido=request.POST.get('apelido'),
                custo_hora=custo
            )
            maq.save()
    
    form = NovaMaquina()
    return render(request, 'main/registro/nova_maquina.html', {'form':form, 'index':index})

def editar_maquina(request, index):
    maq = Maquina.objects.get(id=index)
    form = NovaMaquina({
        'nome':maq.nome,
        'apelido':maq.apelido,
        'custo_hora':maq.custo_hora
    })

    if request.method == 'POST':
        if request.POST.get('salvar'):
            custo = 0
            if request.POST.get('custo_hora'):
                custo = float(request.POST.get('custo_hora'))
            maq.nome=request.POST.get('nome')
            maq.apelido=request.POST.get('apelido')
            maq.custo_hora=custo
            maq.save()
            return redirect(registro)
    return render(request, 'main/registro/maquina.html', {'form':form, 'index':index, 'maquina':maq})

def fila(request):
    if request.method == 'GET':
        if request.POST.get('abrir'):
            pass
            

    maquinas = Maquina.objects.all()
    return render(request, 'main/fila.html', {'maquinas':maquinas})

def nova_peca(request):
    if request.method == 'POST':
        if request.POST.get('salvar'):
            peca = Peca(
                cod_local=request.POST.get('codigo_local'),
                cod_estrangeiro=request.POST.get('codigo_estrangeiro'),
                descricao=request.POST.get('descricao')
            )
            peca.save()
 
            ops = int(request.POST.get('qtd_operacoes'))
            for i in range(ops):
                n = (i+1)*10
                op = Operacao(
                    peca=peca,
                    numero=n,
                    tempo_producao=0,
                    tempo_ajuste=0
                )
                op.save()

    form = NovaPeca()
    return render(request, 'main/registro/nova_peca.html', {'form':form})

def editar_peca(request, index=None):
    peca = Peca.objects.get(cod_local=index)
    ops = len(Operacao.objects.filter(peca=index))
    form = EditarPeca({
        'codigo_estrangeiro':peca.cod_estrangeiro,
        'qtd_operacoes':ops,
        'descricao': peca.descricao    
    })


    if request.method == 'POST':
        if request.POST.get('salvar'):
            ops = int(request.POST.get('qtd_operacoes'))

            if ops != len(Operacao.objects.filter(peca=index)):
                Operacao.objects.filter(peca=index).delete()
                for i in range(ops):
                    n = (i+1)*10
                    op = Operacao(
                        peca=peca,
                        numero=n,
                        tempo_producao=0,
                        tempo_ajuste=0
                    )
                    op.save()

            peca.cod_estrangeiro = request.POST.get('codigo_estrangeiro')
            peca.descricao = request.POST.get('descricao')
            peca.save()
            return redirect('registro')

        if request.POST.get('salvar_ops'):
            ops = int(request.POST.get('qtd_operacoes'))

            if ops != len(Operacao.objects.filter(peca=index)):
                Operacao.objects.filter(peca=index).delete()
                for i in range(ops):
                    n = (i+1)*10
                    op = Operacao(
                        peca=peca,
                        numero=n,
                        tempo_producao=0,
                        tempo_ajuste=0
                    )
                    op.save()

            peca.cod_estrangeiro = request.POST.get('codigo_estrangeiro')
            peca.descricao = request.POST.get('descricao')
            peca.save()

            return redirect('operacoes', index=index)




    return render(request, 'main/registro/peca.html', {'form':form, 'index':index})

def operacoes(request, index=None):
    peca = Peca.objects.get(cod_local=index)
    operacoes = Operacao.objects.filter(peca_id=index)
    
    op_maq_list = {}
    for op in operacoes:
        op_maq_list[op.numero] = []
        for op_maq in OperacaoMaquina.objects.filter(operacao_id=op):
            op_maq_list[op.numero].append(op_maq.maquina.id)
        
    maquinas = Maquina.objects.all()
    message = None
    if request.method == 'POST':
        if request.POST.get('salvar'):
            flag = False
            for op in operacoes:
                op.tempo_producao = request.POST.get(f't_producao{op.numero}')
                op.tempo_ajuste = int(request.POST.get(f't_ajuste{op.numero}')) * 60
                op.save()
                
                for maq in maquinas:
                    query = OperacaoMaquina.objects.filter(Q(maquina=maq) & Q(operacao=op))
                    if request.POST.get(f'op{op.numero}_maq{maq.id}') == 'clicked' and not query:
                        opm = OperacaoMaquina(
                            maquina = maq,
                            operacao = op
                        )
                        opm.save()
                    elif request.POST.get(f'op{op.numero}_maq{maq.id}') != 'clicked' and query:
                        query.delete()

            return redirect(registro)

    return render(request, 'main/registro/operacao.html', {
        'peca':peca,
        'operacoes':operacoes, 
        'index':index, 
        'maquinas':maquinas, 
        'message':message,
        'op_maq_list':op_maq_list
        })
    
def atualizar_pedido(request, index=None):
    msg = ''
    
        
    if not index:
        return redirect(pedidos)
    
    pedido = Pedido.objects.get(id=index)
    fops = FilaOperacao.objects.filter(pedido=pedido)
    
    peca_op = dict()

    for fop in fops:
        peca_op[fop.operacao.peca] = []
    
    for fop in fops:
        op = Operacao.objects.get(id=fop.operacao.pk)
        peca = Peca.objects.get(cod_local=op.peca.pk)


        if peca in peca_op.keys():
            peca_op[peca].append(op)

    if request.method == "POST":
        try:
            count_feitos = 0
            for fop in fops:
                qtd = request.POST.get(f'fop-{fop.id}')
                if int(qtd) == PedidoPeca.objects.get(Q(peca=fop.operacao.peca.cod_local) & Q(pedido=fop.pedido)).quantidade and fop.peso > -1:
                    count_feitos += 1
                    abaixar = FilaOperacao.objects.filter(Q(maquina=fop.maquina) & Q(peso__gt=fop.peso))
                    for a in abaixar:
                        a.peso -= 1
                        a.save()
                    fop.peso = -1
                elif int(qtd) > PedidoPeca.objects.get(Q(peca=fop.operacao.peca.cod_local) & Q(pedido=fop.pedido)).quantidade:
                    raise Exception(f'Quantidade "{int(qtd)}" é inválida.')
                fop.quantidade_feita = int(qtd)
                fop.save()
            
            if count_feitos == len(fops):
                pedido.finalizado = True
                pedido.save()
        except Exception as ex:
            msg = ex

    return render(request, 'main/atualizar-pedido.html', {'pedido':pedido, 'fops':fops, 'msg':msg} )

def pedidos(request):

    pedidos = Pedido.objects.all()
    progresso =  dict()
    for pedido in pedidos:
        qtds = []
        for fop in FilaOperacao.objects.filter(pedido=pedido):
            qtds.append(fop.quantidade_feita)
        progresso[pedido] =  str(round(sum(qtds) / len(qtds), 1)) + '%'

    return render(request, 'main/pedidos.html', {'pedidos':pedidos, 'progresso':progresso})

def novo_pedido(request):
    message = ''
    if request.method == 'POST':
        form = NovoPedido(data=request.POST)
        maquinas = dict()
        inserir_op = dict()
        for i, maq in enumerate(Maquina.objects.all()):
            maquinas[maq] = len(FilaOperacao.objects.filter(maquina=maq))
            inserir_op[maq] = []

        if request.POST.get('salvar'):
            c = 0
            cods = []
            qtds = []
            for i in request.POST.dict():
                if i[:9] == 'cod_local':
                    cods.append(request.POST.get(f'cod_local_{c}'))
                    qtds.append(request.POST.get(f'qtd_{c}'))
                    c += 1
            try:
                datetime.datetime.strptime(request.POST.get('data_entrega'), '%d/%m/%Y')
            except:
                message = 'Data inválida'
                return render(request, 'main/novo-pedido.html', {'form':form, 'message':message, 'c':range(c), 'cods':cods, 'qtds':qtds})
            
            for i in range(c):
                try:
                    Peca.objects.get(cod_local=request.POST.get(f'cod_local_{i}'))
                except Exception as e:
                    message = f'Peça "{ request.POST.get("cod_local_"+str(i)) }" inválida'
                    return render(request, 'main/novo-pedido.html', {'form':form, 'message':message, 'c':range(c), 'cods':cods, 'qtds':qtds})

            pedido = Pedido(
                codigo=request.POST.get('codigo'),
                data_entrega=datetime.datetime.strptime(request.POST.get('data_entrega'), '%d/%m/%Y').date(),
                finalizado=False
            )
            pedido.save()

            op_lst = []

            for i in range(c):
                peca = Peca.objects.get(cod_local=request.POST.get(f'cod_local_{i}'))
                pp = PedidoPeca(
                    pedido=pedido,
                    quantidade=request.POST.get(f'qtd_{i}'),
                    peca=peca
                )
                pp.save()
                for op in Operacao.objects.filter(peca=peca):
                    op_lst.append(op)
                    

            for op in sorted(op_lst, key= lambda op: op.numero):
                minima = None
                for op_maq in OperacaoMaquina.objects.filter(operacao=op):
                    if minima == None:
                        minima = op_maq.maquina
                    elif maquinas[minima] > maquinas[op_maq.maquina]:
                        minima = op_maq.maquina
                maquinas[minima] += 1
                inserir_op[minima].append(op)


            flag = False
            for p in Pedido.objects.all().order_by('data_entrega'):
                # talvez comparar p com pedido, para evitar duplicidade
                if not p.finalizado and pedido.data_entrega < p.data_entrega:
                    flag = True
                    for maq, ops in inserir_op.items():
                        for op in ops:
                            w = FilaOperacao.objects.filter(maquina=minima).count()

                            for p_fop in FilaOperacao.objects.filter(Q(pedido=p) & Q(maquina=maq)):
                                if p_fop.peso < w:
                                    w = p_fop.peso
                                p_fop.peso += 1
                                p_fop.save()

                            fop = FilaOperacao(
                                pedido=pedido,
                                maquina=maq,
                                operacao=op,
                                quantidade_feita=0,
                                peso=w
                            )
                            fop.save()
                    break

            if not flag:
                for maq, ops in inserir_op.items():
                    for op in ops:
                        fop = FilaOperacao(
                                pedido=pedido,
                                maquina=maq,
                                operacao=op,
                                quantidade_feita=0,
                                peso=FilaOperacao.objects.filter(maquina=minima).count()
                            )
                        fop.save()
                

    form = NovoPedido()
    return render(request, 'main/novo-pedido.html', {'form':form, 'message':message})
