from django.urls import path
# Importe o 'views' para que 'views.ProdutoDeleteView' funcione
from . import views 
from .views import (
    ProdutoListView,
    ProdutoCreateView,
    ProdutoDetailView,
    ProdutoUpdateView, 
    CategoriaCreateAjaxView,
    AvaliarProdutoView,
    CurtirProdutoView,
    ProdutoDeleteView,
    )

app_name = 'produto'

urlpatterns = [
    path('', ProdutoListView.as_view(), name='produto_list'),
    path('novo/', ProdutoCreateView.as_view(), name='produto_create'),
    path('<int:pk>/', ProdutoDetailView.as_view(), name='produto_detail'),
    path('<int:produto_id>/avaliar/', AvaliarProdutoView.as_view(), name='avaliar'),
    path('<int:produto_id>/curtir/', CurtirProdutoView.as_view(), name='curtir'),
    path('editar/<int:pk>/', ProdutoUpdateView.as_view(), name='produto_update'),
    path('categoria/nova/', CategoriaCreateAjaxView.as_view(), name='categoria_create_ajax'),
    path('excluir/<int:pk>/', ProdutoDeleteView.as_view(), name='produto_delete'),
]