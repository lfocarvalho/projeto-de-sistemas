from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import Agendamento
from .forms import AgendamentoForm
from loja.models import Loja
from django.utils import timezone


class CriarAgendamento(LoginRequiredMixin, View):
    def get(self, request, loja_id):
        loja = get_object_or_404(Loja, pk=loja_id)
        form = AgendamentoForm(loja_id=loja_id)
        context = {
            'form': form,
            'loja': loja
        }
        return render(request, 'agendamento/criar_agendamento.html', context)

    def post(self, request, loja_id):
        loja = get_object_or_404(Loja, pk=loja_id)
        form = AgendamentoForm(request.POST, loja_id=loja_id)
        if form.is_valid():
            agendamento = form.save(commit=False)
            agendamento.usuario = request.user
            agendamento.loja = loja
            agendamento.status = 'PENDENTE'
            agendamento.save()
            
            messages.success(request, "Agendamento solicitado com sucesso! Aguarde a confirmação.")
            return redirect('agendamento:listar_agendamento')

        context = {
            'form': form,
            'loja': loja
        }
        return render(request, 'agendamento/criar_agendamento.html', context)


class ListarAgendamento(LoginRequiredMixin, View):
    def get(self, request):
        agendamentos_futuros = Agendamento.objects.filter(
            usuario=request.user,
            status__in=['PENDENTE', 'CONFIRMADO']
        ).order_by('data_hora')

        agendamentos_passados = Agendamento.objects.filter(
            usuario=request.user,
            status__in=['CONCLUIDO', 'CANCELADO']
            ).order_by('-data_hora')
        
        context = {
            'agendamentos_futuros': agendamentos_futuros,
            'agendamentos_passados': agendamentos_passados

        }

        return render(request, 'agendamento/listar_agendamentos.html', context)

