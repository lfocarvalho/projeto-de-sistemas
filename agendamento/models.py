from django.db import models
from django.contrib.auth.models import User
from loja.models import Loja
from produto.models import Produto

class Agendamento(models.Model):
    
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CONCLUIDO', 'Concluído'),
        ('CANCELADO', 'Cancelado'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agendamentos")
    
    loja = models.ForeignKey(Loja, on_delete=models.CASCADE, related_name="agendamentos")
    
    produto = models.ForeignKey(Produto, on_delete=models.SET_NULL, null=True, blank=True, related_name="agendamentos")

    data_hora = models.DateTimeField(verbose_name="Data e Hora")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_hora']
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"

    def __str__(self):
        return f"Agendamento de {self.usuario.username} em {self.loja.nome} para {self.data_hora.strftime('%d/%m/%Y %H:%M')}"