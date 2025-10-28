# -*- coding: utf-8 -*-
from django.views.generic import ListView, CreateView, View, DetailView
from django.urls import reverse_lazy
from django.forms import Select, TextInput, Textarea, NumberInput, CheckboxInput, FileInput, EmailInput, TimeInput, URLInput
from .models import Loja, Avaliacao, LojaFavorita
from django.http import JsonResponse
from produto.models import Produto, Categoria
from produto.consts import ANIMAL_CHOICES, PORTE_CHOICES, IDADE_CHOICES
from django.db.models import Q
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from loja.forms import FormularioLoja
from django.shortcuts import render, get_object_or_404, redirect
from .forms import AvaliacaoForm
from django.contrib.auth.decorators import login_required


class ListarLojas(LoginRequiredMixin, ListView):
    """
    View para listar lojas parceiras cadastradas, com filtro de favoritas.
    """
    model = Loja
    template_name = 'loja/loja_list.html'
    login_url = reverse_lazy('login')
    context_object_name = 'lista_lojas'

    def get_queryset(self):
        queryset = super().get_queryset().order_by('nome')
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(Q(nome__icontains=query) | Q(endereco__icontains=query))
        
        favoritas = self.request.GET.get('favoritas')
        if favoritas:
            queryset = queryset.filter(favoritada_por=self.request.user)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['favoritas_usuario'] = [
                loja.id for loja in context['lista_lojas']
                if loja.favoritada_por.filter(id=self.request.user.id).exists()
            ]
        else:
            context['favoritas_usuario'] = []
        return context



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

        context['avaliacoes'] = loja.avaliacoes.select_related('usuario').order_by('-criado_em')
        user = self.request.user
        if user.is_authenticated:
            context['ja_avaliou'] = loja.avaliacoes.filter(usuario=user).exists()
        else:
            context['ja_avaliou'] = False

        if user.is_authenticated:
            context['favoritada'] = LojaFavorita.objects.filter(loja=loja, usuario=user).exists()
        else:
            context['favoritada'] = False

        return context
    
    
@login_required
def avaliar_loja(request, loja_id):
    loja = get_object_or_404(Loja, id=loja_id)

    if request.method == 'POST':
        nota = int(request.POST.get('nota', 0))
        comentario = request.POST.get('comentario', '').strip()

        Avaliacao.objects.update_or_create(
            usuario=request.user,
            loja=loja,
            defaults={'nota': nota, 'comentario': comentario}
        )

        loja.atualizar_media()
        return redirect('loja:loja_detail', pk=loja.id)

    return redirect('loja:loja_detail', pk=loja.id)

@login_required
def favoritar_loja(request, loja_id):
    loja = Loja.objects.get(pk=loja_id)
    if request.user in loja.favoritada_por.all():
        loja.favoritada_por.remove(request.user)
        favoritado = False
    else:
        loja.favoritada_por.add(request.user)
        favoritado = True

    total_favoritos = loja.favoritada_por.count()
    return JsonResponse({'favoritado': favoritado, 'total_favoritos': total_favoritos})


@login_required
def mapa_lojas_view(request):
    """
    View para exibir o mapa com a localização das lojas.
    """
    return render(request, 'loja/mapa_lojas.html')

@login_required
def perfil_usuario(request):
    """
    Exibe a página de perfil do usuário com suas informações e atividades.
    """
    user = request.user
    lojas_favoritas = user.lojas_favoritadas.all().order_by('nome')
    avaliacoes_usuario = Avaliacao.objects.filter(usuario=user).select_related('loja').order_by('-criado_em')

    context = {
        'lojas_favoritas': lojas_favoritas,
        'avaliacoes': avaliacoes_usuario,
        'total_favoritos': lojas_favoritas.count(),
        'total_avaliacoes': avaliacoes_usuario.count(),
        'titulo': 'Meu Perfil',
    }
    return render(request, 'loja/perfil_usuario.html', context)
