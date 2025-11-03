# agendamento/urls.py

from django.urls import path
from .views import CriarAgendamento, ListarAgendamento

app_name = 'agendamento'

urlpatterns = [
    path('lojas/<int:loja_id>/agendar/', CriarAgendamento.as_view(), name='criar_agendamento'),
    path('listar_agendamentos/', ListarAgendamento.as_view(), name='listar_agendamento'),
]