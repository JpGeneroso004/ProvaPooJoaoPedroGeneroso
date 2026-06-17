from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
import json
from .models import Evento
from .forms import EventoForm
from inventario.models import Tenda, ConjuntoPalco


def dashboard(request):
    hoje = timezone.localdate()
    eventos = Evento.objects.all()

    total_eventos = eventos.count()
    ativos     = eventos.filter(status__in=['agendado', 'em_andamento']).count()
    concluidos = eventos.filter(status='concluido').count()
    cancelados = eventos.filter(status='cancelado').count()

    proximos     = eventos.filter(data_inicio__gte=hoje, status='agendado').order_by('data_inicio')[:5]
    em_andamento = eventos.filter(status='em_andamento').order_by('data_fim')

    total_tendas       = Tenda.objects.count()
    tendas_disponiveis = Tenda.objects.filter(status='disponivel').count()
    tendas_em_uso      = Tenda.objects.filter(status='em_uso').count()

    todos_conjuntos = ConjuntoPalco.objects.all()
    placas_em_uso      = sum(c.quantidade_placas for c in todos_conjuntos if c.status == 'em_uso')
    placas_manutencao  = sum(c.quantidade_placas for c in todos_conjuntos if c.status == 'manutencao')
    placas_disponiveis = max(0, 30 - placas_em_uso - placas_manutencao)

    eventos_mapa = []
    for e in eventos.filter(latitude__isnull=False, longitude__isnull=False):
        eventos_mapa.append({
            'nome': e.nome, 'cliente': e.cliente,
            'local': e.local, 'cidade': e.cidade,
            'data_inicio': str(e.data_inicio), 'data_fim': str(e.data_fim),
            'status': e.get_status_display(), 'status_key': e.status,
            'tendas': e.total_tendas(), 'placas': e.total_placas(),
            'lat': float(e.latitude), 'lng': float(e.longitude),
            'url': f'/eventos/{e.pk}/',
        })

    context = {
        'total_eventos': total_eventos, 'ativos': ativos,
        'concluidos': concluidos, 'cancelados': cancelados,
        'proximos': proximos, 'em_andamento': em_andamento,
        'total_tendas': total_tendas,
        'tendas_disponiveis': tendas_disponiveis, 'tendas_em_uso': tendas_em_uso,
        'placas_em_uso': placas_em_uso, 'placas_disponiveis': placas_disponiveis,
        'eventos_mapa_json': json.dumps(eventos_mapa, ensure_ascii=False),
    }
    return render(request, 'eventos/dashboard.html', context)


def lista_eventos(request):
    q = request.GET.get('q', '').strip()
    status = request.GET.get('status', '')
    eventos = Evento.objects.all()
    if q:
        eventos = eventos.filter(
            Q(nome__icontains=q) | Q(cliente__icontains=q) |
            Q(local__icontains=q) | Q(cidade__icontains=q))
    if status:
        eventos = eventos.filter(status=status)
    return render(request, 'eventos/lista.html', {'eventos': eventos, 'q': q, 'status': status})


def detalhe_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    evento_mapa = None
    if evento.latitude and evento.longitude:
        evento_mapa = json.dumps([{
            'nome': evento.nome, 'cliente': evento.cliente,
            'local': evento.local, 'cidade': evento.cidade,
            'data_inicio': str(evento.data_inicio), 'data_fim': str(evento.data_fim),
            'status': evento.get_status_display(), 'status_key': evento.status,
            'tendas': evento.total_tendas(), 'placas': evento.total_placas(),
            'lat': float(evento.latitude), 'lng': float(evento.longitude),
            'url': f'/eventos/{evento.pk}/',
        }], ensure_ascii=False)
    return render(request, 'eventos/detalhe.html', {'evento': evento, 'evento_mapa_json': evento_mapa})


def novo_evento(request):
    if request.method == 'POST':
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save()
            evento.tendas.all().update(status='em_uso')
            evento.conjuntos.all().update(status='em_uso')
            messages.success(request, f'Evento "{evento.nome}" criado com sucesso!')
            return redirect('eventos:detalhe', pk=evento.pk)
    else:
        form = EventoForm()
    return render(request, 'eventos/form_evento.html', {'form': form, 'titulo': 'Novo Evento'})


def editar_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        tendas_antigas    = list(evento.tendas.all())
        conjuntos_antigos = list(evento.conjuntos.all())
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            for t in tendas_antigas:
                t.status = 'disponivel'; t.save()
            for c in conjuntos_antigos:
                c.status = 'disponivel'; c.save()
            evento = form.save()
            if evento.status in ['agendado', 'em_andamento']:
                evento.tendas.all().update(status='em_uso')
                evento.conjuntos.all().update(status='em_uso')
            messages.success(request, 'Evento atualizado com sucesso!')
            return redirect('eventos:detalhe', pk=evento.pk)
    else:
        form = EventoForm(instance=evento)
    return render(request, 'eventos/form_evento.html', {
        'form': form, 'titulo': 'Editar Evento', 'evento': evento})


def excluir_evento(request, pk):
    evento = get_object_or_404(Evento, pk=pk)
    if request.method == 'POST':
        evento.tendas.all().update(status='disponivel')
        evento.conjuntos.all().update(status='disponivel')
        nome = evento.nome
        evento.delete()
        messages.success(request, f'Evento "{nome}" removido com sucesso!')
        return redirect('eventos:lista')
    return render(request, 'eventos/confirmar_exclusao.html', {'evento': evento})
