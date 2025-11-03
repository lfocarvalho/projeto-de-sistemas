from django.urls import reverse_lazy
# DeleteView foi adicionado aqui
from django.views.generic import ListView, CreateView, DetailView, UpdateView, View, DeleteView
from django.forms import Select, TextInput, Textarea, NumberInput, CheckboxInput, FileInput
from django.http import JsonResponse, HttpResponseBadRequest
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.db.models import Min, Max, Count, Q, Avg
from .forms import ProdutoForm

from .models import Produto, Categoria, Loja, AvaliacaoProduto
from .forms import CategoriaForm, ProdutoForm, Categoria
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
            loja_count=Count('loja', distinct=True),
            avg_avaliacao=Avg('avaliacoes__nota'),
            categoria_nome=Min('categoria__nome')
        ).order_by('nome')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias'] = Categoria.objects.all()
        context['animal_choices'] = ANIMAL_CHOICES
        
        # ADICIONADO: Passa a informação se o usuário é admin
        context['is_admin'] = self.request.user.is_authenticated and self.request.user.is_superuser
        
        if self.request.user.is_authenticated:
            # Pega os IDs dos produtos que o usuário já curtiu
            produtos_curtidos_ids = self.request.user.produtos_curtidos.values_list('id', flat=True)
            # Filtra os produtos da página atual que estão na lista de curtidos
            produtos_na_pagina_ids = [p['id'] for p in context['produtos']]
            context['curtidos_usuario'] = list(set(produtos_curtidos_ids) & set(produtos_na_pagina_ids))
            context['is_store_user'] = Loja.objects.filter(email=self.request.user.email).exists()
        return context


class ProdutoFormMixin:
    """
    Mixin para compartilhar a lógica de formulário entre Create e Update.
    """
    def get_form(self, form_class=None):
        """
        Adiciona classes CSS aos campos do formulário para estilização com Bootstrap.
        """
        form = super().get_form(form_class)

        # Para o lojista, removemos o campo 'loja' ANTES de iterar para evitar o RuntimeError.
        if not self.request.user.is_superuser and 'loja' in form.fields:
            del form.fields['loja']

        # Agora, iteramos sobre os campos restantes para aplicar os estilos.
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


class ProdutoCreateView(LoginRequiredMixin, UserPassesTestMixin, ProdutoFormMixin, CreateView):
    """
    View para cadastrar um novo produto.
    """
    model = Produto
    form_class = ProdutoForm
    template_name = 'produto/produto_form.html'
    success_url = reverse_lazy('produto:produto_list')
    login_url = reverse_lazy('login')

    def test_func(self):
        """Permite acesso a superusuários ou usuários associados a uma loja."""
        if self.request.user.is_superuser:
            return True
        return Loja.objects.filter(email=self.request.user.email).exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Cadastrar Novo Produto'
        # Adiciona o formulário de categoria ao contexto se o usuário for admin
        if self.request.user.is_superuser:
            context['categoria_form'] = CategoriaForm()
        return context

    def post(self, request, *args, **kwargs):
        """
        Sobrescreve o método post para manipular o formulário antes da validação.
        """
        form = self.get_form()
        if not request.user.is_superuser:
            # Se for um lojista, busca a loja e a atribui à instância do formulário ANTES de validar.
            try:
                loja_usuario = Loja.objects.get(email=request.user.email)
                form.instance.loja = loja_usuario
            except Loja.DoesNotExist:
                form.add_error(None, "Não foi possível encontrar uma loja associada a este email.")
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
        A lógica de atribuição da loja foi movida para o método post.
        Este método agora apenas salva o formulário.
        """
        return super().form_valid(form)


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
        produto = self.get_object()
        ofertas = Produto.objects.filter(nome__iexact=produto.nome, disponivel=True).order_by('preco')
        context['ofertas'] = ofertas
        
        # ADICIONADO: Passa a informação se o usuário é admin
        context['is_admin'] = self.request.user.is_authenticated and self.request.user.is_superuser
        
        # Avaliações
        context['avaliacoes'] = produto.avaliacoes.select_related('usuario').all()
        if self.request.user.is_authenticated:
            context['ja_avaliou'] = AvaliacaoProduto.objects.filter(produto=produto, usuario=self.request.user).exists()
            context['curtido'] = produto.curtido_por.filter(pk=self.request.user.pk).exists()
        return context


class AvaliarProdutoView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        produto_id = kwargs.get('produto_id')
        try:
            produto = Produto.objects.get(pk=produto_id)
        except Produto.DoesNotExist:
            return HttpResponseBadRequest('Produto inválido')

        nota = int(request.POST.get('nota', 0))
        comentario = request.POST.get('comentario', '').strip() or None
        if nota < 1 or nota > 5:
            return HttpResponseBadRequest('Nota inválida')

        avaliacao, created = AvaliacaoProduto.objects.update_or_create(
            produto=produto,
            usuario=request.user,
            defaults={'nota': nota, 'comentario': comentario}
        )
        produto.atualizar_media()
        return JsonResponse({
            'success': True,
            'media': produto.avaliacao_media,
            'nota': avaliacao.nota,
            'created': created,
        })


class CurtirProdutoView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')

    def post(self, request, *args, **kwargs):
        produto_id = kwargs.get('produto_id')
        try:
            produto = Produto.objects.get(pk=produto_id)
        except Produto.DoesNotExist:
            return HttpResponseBadRequest('Produto inválido')

        user = request.user
        if produto.curtido_por.filter(pk=user.pk).exists():
            produto.curtido_por.remove(user)
            curtido = False
        else:
            produto.curtido_por.add(user)
            curtido = True
        return JsonResponse({'curtido': curtido, 'total_curtidas': produto.curtido_por.count()})


class ProdutoUpdateView(LoginRequiredMixin, UserPassesTestMixin, ProdutoFormMixin, UpdateView):
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



class AdminRequiredMixin(UserPassesTestMixin):
    """
    Garante que o usuário logado é um superusuário.
    """
    def test_func(self):
        return self.request.user.is_superuser

class ProdutoDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """
    View para um admin excluir um produto.
    """
    model = Produto
    template_name = 'produto/produto_confirm_delete.html'
    context_object_name = 'produto'
    
    def get_success_url(self):
        # Volta para a página da loja de onde o produto era
        loja_pk = self.object.loja.pk
        return reverse_lazy('loja:loja_detail', kwargs={'pk': loja_pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Excluir Produto: {self.object.nome}'
        return context