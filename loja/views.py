# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView, View
from django.urls import reverse_lazy
<<<<<<< Updated upstream
from loja.models import Loja
=======
from django.forms import Select, TextInput, Textarea, NumberInput, CheckboxInput, FileInput, EmailInput, TimeInput, URLInput
from .models import Loja
from produto.models import Produto, Categoria
from produto.consts import ANIMAL_CHOICES, PORTE_CHOICES, IDADE_CHOICES
>>>>>>> Stashed changes
from django.db.models import Q
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from loja.forms import FormularioLoja


class ListarLojas(LoginRequiredMixin, ListView):
    """
    View para listar lojas parceiras cadastradas.
    """
    model = Loja
<<<<<<< Updated upstream
=======
    template_name = 'loja/loja_list.html'
    login_url = reverse_lazy('login')
>>>>>>> Stashed changes
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
    success_url = reverse_lazy('loja:loja_list')

    def get_form(self, form_class=None):
        """
        Adiciona classes CSS aos campos do formulário para estilização com Bootstrap.
        """
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            widget = field.widget
            if isinstance(widget, Select):
                widget.attrs.update({'class': 'form-select'})
            elif isinstance(widget, CheckboxInput):
                 widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(widget, (TextInput, Textarea, NumberInput, FileInput, EmailInput, TimeInput, URLInput)):
                widget.attrs.update({'class': 'form-control'})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cadastrar Nova Loja'
        return context

<<<<<<< Updated upstream
=======



class LojaDetailView(LoginRequiredMixin, DetailView):
    """
    View para exibir os detalhes de uma loja e seus produtos, com filtros.
    """
    model = Loja
    template_name = 'loja/loja_detail.html'
    login_url = reverse_lazy('login')
    context_object_name = 'loja'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loja = self.get_object()
        
        # Pega os parâmetros de filtro da requisição GET
        search_query = self.request.GET.get('q', '')
        categoria_query = self.request.GET.get('categoria', '')
        animal_query = self.request.GET.get('animal', '')
        preco_min_query = self.request.GET.get('preco_min', '')
        preco_max_query = self.request.GET.get('preco_max', '')

        # Começa com todos os produtos disponíveis da loja
        produtos = Produto.objects.filter(loja=loja, disponivel=True)
        
        # Aplica os filtros se eles existirem
        if search_query:
            produtos = produtos.filter(nome__icontains=search_query)
        if categoria_query:
            produtos = produtos.filter(categoria__id=categoria_query)
        if animal_query:
            produtos = produtos.filter(animal_destino=animal_query)
        if preco_min_query:
            produtos = produtos.filter(preco__gte=preco_min_query)
        if preco_max_query:
            produtos = produtos.filter(preco__lte=preco_max_query)

        # Adiciona os produtos filtrados e as opções de filtro ao contexto
        context['produtos'] = produtos.distinct()
        context['categorias'] = Categoria.objects.all()
        context['animal_choices'] = ANIMAL_CHOICES
        context['porte_choices'] = PORTE_CHOICES
        context['idade_choices'] = IDADE_CHOICES
        return context
>>>>>>> Stashed changes
