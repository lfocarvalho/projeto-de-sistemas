from django.contrib import admin
from .models import Categoria, Produto


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    """
    Configuração da interface de administração para o modelo Categoria.
    """
    list_display = ('nome', 'descricao')
    search_fields = ('nome',)


@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    """
    Configuração da interface de administração para o modelo Produto.
    """
    list_display = ('nome', 'loja', 'categoria', 'preco', 'estoque', 'disponivel', 'animal_destino')
    search_fields = ('nome', 'descricao', 'loja__nome')
    list_filter = ('disponivel', 'categoria', 'loja', 'animal_destino', 'porte_animal', 'idade_animal')
    list_editable = ('preco', 'estoque', 'disponivel')
    autocomplete_fields = ('loja', 'categoria')
