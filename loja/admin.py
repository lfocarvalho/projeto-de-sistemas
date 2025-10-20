from django.contrib import admin
from .models import Loja, CarouselImage


@admin.register(Loja)
class LojaAdmin(admin.ModelAdmin):
    """
    Configuração da interface de administração para o modelo Loja.
    """
    list_display = ('nome', 'telefone', 'email', 'website', 'horario_abertura', 'horario_fechamento')
    search_fields = ('nome', 'endereco')
    list_filter = ('horario_abertura', 'horario_fechamento')


@admin.register(CarouselImage)
class CarouselImageAdmin(admin.ModelAdmin):
    list_display = ('caption_title', 'order', 'image')
    list_editable = ('order',)


# A linha abaixo faz o mesmo que o @admin.register(Loja) acima.
# admin.site.register(Loja, LojaAdmin)
