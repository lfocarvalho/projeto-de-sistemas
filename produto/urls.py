from django.urls import path
from .views import ProdutoListView, ProdutoCreateView, CategoriaCreateAjaxView

app_name = 'produto'

urlpatterns = [
    path('', ProdutoListView.as_view(), name='produto_list'),
    path('novo/', ProdutoCreateView.as_view(), name='produto_create'),
    path('categorias/nova/ajax/', CategoriaCreateAjaxView.as_view(), name='categoria_create_ajax'),
    # Futuramente, você pode adicionar rotas para editar e deletar
    # path('<int:pk>/editar/', ProdutoUpdateView.as_view(), name='produto_update'),
]