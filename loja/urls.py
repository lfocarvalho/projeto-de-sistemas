from django.urls import path
from .views import ListarLojas, LojaDetailView

# Adiciona um namespace para o app 'loja'
app_name = 'loja'

urlpatterns = [
    # A rota para listar lojas, que agora será acessível como 'loja:loja_list'
    path('', ListarLojas.as_view(), name='loja_list'),
    # Nova rota para os detalhes da loja, que recebe o ID (pk) da loja
    path('<int:pk>/', LojaDetailView.as_view(), name='loja_detail'),
]