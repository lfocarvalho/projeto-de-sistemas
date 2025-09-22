# -*- coding: utf-8 -*-
from django.views.generic import ListView
from loja.models import Loja
from django.db.models import Q


class ListarLojas(ListView):
    """
    View para listar lojas parceiras cadastradas.
    """
    model = Loja
    context_object_name = 'lista_lojas'
    template_name = 'loja/loja_list.html'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('nome')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) |
                Q(endereco__icontains=query)
            )
        return queryset