from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Tenda, ConjuntoPalco
from .forms import TendaForm, ConjuntoPalcoForm


def inventario(request):
    tendas = Tenda.objects.all().order_by('tamanho', 'tipo', 'codigo')

    tendas_disponiveis = tendas.filter(status='disponivel').count()
    tendas_em_uso      = tendas.filter(status='em_uso').count()
    tendas_manutencao  = tendas.filter(status='manutencao').count()
    total_tendas       = tendas.count()
    total_piramisais   = tendas.filter(tipo='piramidal').count()
    total_chapeu       = tendas.filter(tipo='chapeu_bruxa').count()
    piramisais_disponiveis = tendas.filter(tipo='piramidal',    status='disponivel').count()
    chapeu_disponiveis     = tendas.filter(tipo='chapeu_bruxa', status='disponivel').count()

    # Conjuntos de palco/piso
    conjuntos = ConjuntoPalco.objects.all()
    total_placas      = sum(c.quantidade_placas for c in conjuntos)
    placas_em_uso     = sum(c.quantidade_placas for c in conjuntos if c.status == 'em_uso')
    placas_manutencao = sum(c.quantidade_placas for c in conjuntos if c.status == 'manutencao')
    placas_disponiveis = max(0, 30 - placas_em_uso - placas_manutencao)

    conjuntos_disponiveis = conjuntos.filter(status='disponivel').count()
    conjuntos_em_uso      = conjuntos.filter(status='em_uso').count()
    conjuntos_manutencao  = conjuntos.filter(status='manutencao').count()

    # Painel visual por tamanho
    ORDEM = ['10x10', '8x8', '7x7', '6x6', '5x5', '4x4', '3x3']
    estoque_resumo = []
    for tam in ORDEM:
        piramisais = list(tendas.filter(tamanho=tam, tipo='piramidal'))
        chapeu     = list(tendas.filter(tamanho=tam, tipo='chapeu_bruxa'))
        if piramisais or chapeu:
            estoque_resumo.append({
                'tamanho': f'Tenda {tam} m',
                'piramisais': piramisais,
                'chapeu': chapeu,
            })

    context = {
        'tendas': tendas,
        'total_tendas': total_tendas,
        'tendas_disponiveis': tendas_disponiveis,
        'tendas_em_uso': tendas_em_uso,
        'tendas_manutencao': tendas_manutencao,
        'total_piramisais': total_piramisais,
        'total_chapeu': total_chapeu,
        'piramisais_disponiveis': piramisais_disponiveis,
        'chapeu_disponiveis': chapeu_disponiveis,
        'estoque_resumo': estoque_resumo,
        'conjuntos': conjuntos,
        'total_placas': total_placas,
        'placas_em_uso': placas_em_uso,
        'placas_disponiveis': placas_disponiveis,
        'placas_manutencao': placas_manutencao,
        'conjuntos_disponiveis': conjuntos_disponiveis,
        'conjuntos_em_uso': conjuntos_em_uso,
        'conjuntos_manutencao': conjuntos_manutencao,
    }
    return render(request, 'inventario/inventario.html', context)


# ── Tendas ────────────────────────────────────────────────
def nova_tenda(request):
    if request.method == 'POST':
        form = TendaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tenda cadastrada com sucesso!')
            return redirect('inventario:inventario')
    else:
        form = TendaForm()
    return render(request, 'inventario/form_tenda.html', {'form': form, 'titulo': 'Nova Tenda'})


def editar_tenda(request, pk):
    tenda = get_object_or_404(Tenda, pk=pk)
    if request.method == 'POST':
        form = TendaForm(request.POST, instance=tenda)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tenda atualizada com sucesso!')
            return redirect('inventario:inventario')
    else:
        form = TendaForm(instance=tenda)
    return render(request, 'inventario/form_tenda.html', {
        'form': form, 'titulo': f'Editar {tenda.codigo}', 'tenda': tenda
    })


def excluir_tenda(request, pk):
    tenda = get_object_or_404(Tenda, pk=pk)
    if request.method == 'POST':
        cod = tenda.codigo
        tenda.delete()
        messages.success(request, f'Tenda {cod} removida com sucesso!')
    return redirect('inventario:inventario')


# ── Conjuntos de Palco/Piso ───────────────────────────────
def novo_conjunto(request):
    if request.method == 'POST':
        form = ConjuntoPalcoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conjunto cadastrado com sucesso!')
            return redirect('inventario:inventario')
    else:
        form = ConjuntoPalcoForm()
    return render(request, 'inventario/form_conjunto.html', {'form': form, 'titulo': 'Novo Conjunto de Palco/Piso'})


def editar_conjunto(request, pk):
    conjunto = get_object_or_404(ConjuntoPalco, pk=pk)
    if request.method == 'POST':
        form = ConjuntoPalcoForm(request.POST, instance=conjunto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conjunto atualizado com sucesso!')
            return redirect('inventario:inventario')
    else:
        form = ConjuntoPalcoForm(instance=conjunto)
    return render(request, 'inventario/form_conjunto.html', {
        'form': form, 'titulo': f'Editar {conjunto.nome}', 'conjunto': conjunto
    })


def excluir_conjunto(request, pk):
    conjunto = get_object_or_404(ConjuntoPalco, pk=pk)
    if request.method == 'POST':
        nome = conjunto.nome
        conjunto.delete()
        messages.success(request, f'Conjunto "{nome}" removido com sucesso!')
    return redirect('inventario:inventario')
