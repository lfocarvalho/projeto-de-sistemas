from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, View
from django.forms import Select, TextInput, Textarea, NumberInput, CheckboxInput, FileInput
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import Produto
from .forms import CategoriaForm

class ProdutoListView(ListView):
    """
    View para listar todos os produtos cadastrados.
    """
    model = Produto
    template_name = 'produto/produto_list.html'
    context_object_name = 'produtos'
    paginate_by = 10  # Adiciona paginação para melhor performance


class ProdutoCreateView(LoginRequiredMixin, CreateView):
    """
    View para cadastrar um novo produto.
    """
    model = Produto
    template_name = 'produto/produto_form.html'
    fields = ['loja', 'categoria', 'nome', 'descricao', 'preco', 'estoque', 'disponivel', 'animal_destino', 'porte_animal', 'idade_animal', 'foto']
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