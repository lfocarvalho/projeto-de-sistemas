from django.urls import path
from .views import ListarLojas, LojaDetailView

# Adiciona um namespace para o app 'loja'
app_name = 'loja'

urlpatterns = [
    path('', ListarLojas.as_view(), name='listar-lojas'),
    path('novo/', CriarLoja.as_view(), name='criar-loja'),
    path('fotos/<str:arquivo>/', FotoLoja.as_view(), name='foto-loja'),
    path('<int:pk>/', LojaDetailView.as_view(), name='loja_detail'),
]