from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View
from django.forms import Select, TextInput, Textarea, NumberInput, CheckboxInput, FileInput, EmailInput, URLInput
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q, Min, Max, F, Subquery, OuterRef

from .models import Produto, Categoria, Loja
from .forms import CategoriaForm
from .consts import ANIMAL_CHOICES

class ProdutoListView(LoginRequiredMixin, ListView):
    """
    View para listar e filtrar produtos, agrupados por nome.
    """
    model = Produto
    template_name = 'produto/produto_list.html'
    login_url = reverse_lazy('login')
    context_object_name = 'produtos'
    paginate_by = 12 # A paginação será aplicada após o processamento

    def get_queryset(self):
        queryset = Produto.objects.filter(disponivel=True)
        
        search_query = self.request.GET.get('q', '')
        categoria_query = self.request.GET.get('categoria', '')
        animal_query = self.request.GET.get('animal', '')

        if search_query:
            queryset = queryset.filter(
                Q(nome__icontains=search_query) | Q(loja__nome__icontains=search_query)
            )
        if categoria_query:
            queryset = queryset.filter(categoria__id=categoria_query)
        if animal_query:
            queryset = queryset.filter(animal_destino=animal_query)

        # Subquery para encontrar o ID do produto com o menor preço para cada nome
        min_price_product_id = Subquery(
            queryset.filter(nome=OuterRef('nome'))
            .order_by('preco')
            .values('id')[:1]
        )

        # Agrupa por nome (case-insensitive) e anota os dados necessários
        grouped_products = queryset.values('nome').annotate(
            min_preco=Min('preco'),
            max_preco=Max('preco'),
            # Pega o ID, foto e categoria do produto de menor preço
            produto_id=min_price_product_id,
            foto=Subquery(queryset.filter(id=min_price_product_id).values('foto')),
            categoria_nome=Subquery(queryset.filter(id=min_price_product_id).values('categoria__nome')),
        ).order_by('nome')

        return grouped_products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['animal_choices'] = ANIMAL_CHOICES
        # Adiciona a flag 'is_store_user' para o template
        if self.request.user.is_authenticated and not self.request.user.is_superuser:
            context['is_store_user'] = Loja.objects.filter(email=self.request.user.email).exists()
        return context


class ProdutoDetailView(LoginRequiredMixin, DetailView):
    """
    View para exibir os detalhes de um único produto.
    """
    model = Produto
    template_name = 'produto/produto_detail.html'
    login_url = reverse_lazy('login')
    context_object_name = 'produto'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto_atual = self.get_object()

        # Busca por todas as ofertas disponíveis para este produto, ordenadas por preço.
        ofertas = Produto.objects.filter(
            nome__iexact=produto_atual.nome,
            disponivel=True
        ).select_related('loja').order_by('preco')

        context['ofertas'] = ofertas
        return context


class ProdutoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    """
    View para cadastrar um novo produto.
    """
    model = Produto
    template_name = 'produto/produto_form.html'
    fields = [
        'loja', 'categoria', 'nome', 'descricao', 'preco', 'estoque', 'disponivel',
        'animal_destino', 'porte_animal', 'idade_animal', 'foto'
    ]
    success_url = reverse_lazy('produto:produto_list')
    login_url = reverse_lazy('login')

    def test_func(self):
        """
        Permite acesso a superusuários ou a usuários que são donos de uma loja.
        """
        if self.request.user.is_superuser:
            return True
        # Verifica se o email do usuário está associado a alguma loja
        return Loja.objects.filter(email=self.request.user.email).exists()

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
    
    def form_valid(self, form):
        """
        Se o usuário não for superuser, define a loja do produto automaticamente.
        """
        if not self.request.user.is_superuser:
            try:
                loja_do_usuario = Loja.objects.get(email=self.request.user.email)
                form.instance.loja = loja_do_usuario
            except Loja.DoesNotExist:
                return HttpResponseForbidden("Você não está associado a nenhuma loja.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cadastrar Novo Produto'
        # Adiciona o formulário de categoria ao contexto se o usuário for admin
        if self.request.user.is_superuser:
            context['categoria_form'] = CategoriaForm()
        # Adiciona a flag 'is_store_user' para o template
        if not self.request.user.is_superuser:
            context['is_store_user'] = Loja.objects.filter(email=self.request.user.email).exists()
        return context


class ProdutoUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    View para que um usuário de loja ou superuser possa editar um produto.
    """
    model = Produto
    template_name = 'produto/produto_form.html'
    fields = [
        'categoria', 'nome', 'descricao', 'preco', 'estoque', 'disponivel',
        'animal_destino', 'porte_animal', 'idade_animal', 'foto'
    ]

    def test_func(self):
        """
        Permite acesso se o usuário for superuser ou se o produto pertencer à sua loja.
        """
        produto = self.get_object()
        if self.request.user.is_superuser:
            return True
        try:
            # Verifica se o produto pertence à loja do usuário logado
            loja_do_usuario = Loja.objects.get(email=self.request.user.email)
            return produto.loja == loja_do_usuario
        except Loja.DoesNotExist:
            return False

    def get_success_url(self):
        # Redireciona para a página de detalhes do produto que acabou de ser editado
        return reverse_lazy('produto:produto_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar: {self.object.nome}'
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for field_name, field in form.fields.items():
            widget = field.widget
            if isinstance(widget, Select):
                widget.attrs.update({'class': 'form-select'})
            elif isinstance(widget, CheckboxInput):
                 widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(widget, (TextInput, Textarea, NumberInput, FileInput, EmailInput, URLInput)):
                widget.attrs.update({'class': 'form-control'})
        return form

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