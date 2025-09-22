from django.contrib import admin
from .models import Loja


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    """
    Configuração da interface de administração para o modelo Loja.
    """
    list_display = ('nome', 'telefone', 'email', 'website')
    search_fields = ('nome', 'endereco')
    list_filter = ('horario_funcionamento',)


# A linha abaixo faz o mesmo que o @admin.register(Loja) acima.
# admin.site.register(Loja, LojaAdmin)
