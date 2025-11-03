from django.urls import path
from .views import ProdutoListView, ProdutoCreateView, CategoriaCreateAjaxView, ProdutoDetailView, ProdutoUpdateView

# Adiciona um namespace para o app 'produto'

app_name = 'produto'

urlpatterns = [
    path('', ProdutoListView.as_view(), name='produto_list'),
    path('novo/', ProdutoCreateView.as_view(), name='produto_create'),
    path('<int:pk>/', ProdutoDetailView.as_view(), name='produto_detail'),
    path('<int:pk>/editar/', ProdutoUpdateView.as_view(), name='produto_update'),
    path('categoria/nova/', CategoriaCreateAjaxView.as_view(), name='categoria_create_ajax'),
]