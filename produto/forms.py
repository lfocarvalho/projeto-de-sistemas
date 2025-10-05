from django import forms
from .models import Categoria


class CategoriaForm(forms.ModelForm):
    """
    Formulário para a criação de uma nova Categoria.
    """
    class Meta:
        model = Categoria
        fields = ['nome', 'descricao']