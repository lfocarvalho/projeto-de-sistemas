from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from django.forms import Select, TextInput, Textarea, NumberInput, CheckboxInput, FileInput
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Min, Max, Count, Q

from .models import Produto, Categoria
from .forms import CategoriaForm, ProdutoForm
from .consts import ANIMAL_CHOICES

class ProdutoListView(LoginRequiredMixin, ListView):
    """
    View para listar e agrupar produtos, funcionando como um comparador de preços.
    """
    model = Produto
    template_name = 'produto/produto_list.html'
    context_object_name = 'produtos'
    login_url = reverse_lazy('login')
    paginate_by = 12

    def get_queryset(self):
        # Inicia a queryset base e aplica os filtros
        queryset = Produto.objects.filter(disponivel=True)
        
        query = self.request.GET.get('q')
        categoria_id = self.request.GET.get('categoria', '')
        animal = self.request.GET.get('animal', '')

        if query:
            queryset = queryset.filter(nome__icontains=query)
        if categoria_id.isdigit():
            queryset = queryset.filter(categoria__id=categoria_id)
        if animal:
            queryset = queryset.filter(animal_destino=animal)

        # Troque 'preco' pelo nome do campo correto se for diferente!
        return queryset.values('nome').annotate(
            min_preco=Min('preco'),
            max_preco=Max('preco'),
            id=Min('id'),
            foto=Min('foto', filter=Q(foto__isnull=False)),
            loja_count=Count('loja', distinct=True)
        ).order_by('nome')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['animal_choices'] = ANIMAL_CHOICES
        return context


class ProdutoCreateView(LoginRequiredMixin, CreateView):
    """
    View para cadastrar um novo produto.
    """
    model = Produto
    form_class = ProdutoForm
    template_name = 'produto/produto_form.html'
    success_url = reverse_lazy('produto:produto_list')
    login_url = reverse_lazy('login')

    def get_form(self, form_class=None):
        """
        Adiciona classes CSS aos campos do formulário para estilização com Bootstrap.
        """
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            widget = field.widget
            # Aplica a classe 'form-select' para campos de seleção (ForeignKey, Choices)
            if isinstance(widget, Select):
                widget.attrs.update({'class': 'form-select'})
            # Aplica a classe 'form-check-input' para campos de checkbox
            elif isinstance(widget, CheckboxInput):
                 widget.attrs.update({'class': 'form-check-input'})
            # Aplica a classe 'form-control' para os demais campos
            elif isinstance(widget, (TextInput, Textarea, NumberInput, FileInput)):
                widget.attrs.update({'class': 'form-control'})
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cadastrar Novo Produto'
        # Adiciona o formulário de categoria ao contexto se o usuário for admin
        if self.request.user.is_superuser:
            context['categoria_form'] = CategoriaForm()
        return context


class ProdutoDetailView(LoginRequiredMixin, DetailView):
    """
    View para exibir os detalhes de um produto e as ofertas em outras lojas.
    """
    model = Produto
    template_name = 'produto/produto_detail.html'
    context_object_name = 'produto'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto_selecionado = self.get_object()
        # Busca todos os produtos com o mesmo nome (ofertas em diferentes lojas)
        ofertas = Produto.objects.filter(nome__iexact=produto_selecionado.nome, disponivel=True).order_by('preco')
        context['ofertas'] = ofertas
        return context


class ProdutoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View para atualizar um produto existente.
    Apenas superusuários ou o dono da loja podem editar.
    """
    model = Produto
    form_class = ProdutoForm
    template_name = 'produto/produto_form.html'
    login_url = reverse_lazy('login')

    def test_func(self):
        produto = self.get_object()
        return self.request.user.is_superuser or self.request.user.email == produto.loja.email

    def get_success_url(self):
        return reverse_lazy('produto:produto_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Produto: {self.object.nome}'
        # Adiciona o formulário de categoria ao contexto para o modal
        if self.request.user.is_superuser:
            context['categoria_form'] = CategoriaForm()
        return context


class CategoriaCreateAjaxView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    View para criar uma nova categoria via AJAX.
    Acessível apenas por superusuários.
    """
    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, *args, **kwargs):
        form = CategoriaForm(request.POST)
        if form.is_valid():
            categoria = form.save()
            return JsonResponse({'success': True, 'id': categoria.id, 'nome': categoria.nome})
        
        # Coleta os erros de validação para retornar no JSON
        errors = {field: error[0] for field, error in form.errors.items()}
        return JsonResponse({'success': False, 'errors': errors}, status=400)