from django import forms
from .models import Categoria, Produto


class CategoriaForm(forms.ModelForm):
    """
    Formulário para a criação de uma nova Categoria.
    """
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']


class ProdutoForm(forms.ModelForm):
    """
    Formulário para a criação e edição de um Produto.
    """
    class Meta:
        model = Produto
        fields = ['loja', 'categoria', 'nome', 'descricao', 'preco', 'estoque', 'disponivel', 'animal_destino', 'porte_animal', 'idade_animal', 'foto']