from django.views.generic import ListView, DetailView, CreateView, View
from django.urls import reverse_lazy
from .models import Loja
from produto.models import Produto, Categoria
from produto.consts import ANIMAL_CHOICES, PORTE_CHOICES, IDADE_CHOICES
from django.db.models import Q
from django.http import FileResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.mixins import LoginRequiredMixin
from loja.forms import FormularioLoja


class ListarLojas(ListView):
    """
    View para listar e pesquisar as lojas.
    """
    model = Loja
    template_name = 'loja/loja_list.html'
    context_object_name = 'lista_lojas'
    paginate_by = 9

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) | Q(endereco__icontains=query)
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




class LojaDetailView(DetailView):
    """
    View para exibir os detalhes de uma loja e seus produtos, com filtros.
    """
    model = Loja
    template_name = 'loja/loja_detail.html'
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