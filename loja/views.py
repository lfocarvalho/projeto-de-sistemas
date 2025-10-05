# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView, View
from django.urls import reverse_lazy
from loja.models import Loja
from django.db.models import Q
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from loja.forms import FormularioLoja


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

class CriarLoja(LoginRequiredMixin, CreateView):
    model = Loja
    form_class = FormularioLoja
    template_name = 'loja/novo.html'
    success_url = reverse_lazy('listar-lojas')

class FotoLoja(View):
    def get(self, request, arquivo):
        try:
            loja = Loja.objects.get(foto='loja/fotos/{}'.format(arquivo))
            return FileResponse(loja.foto)
        except ObjectDoesNotExist:
                raise Http404("Loja não possui foto.")
        except Exception as exception:
            raise exception

