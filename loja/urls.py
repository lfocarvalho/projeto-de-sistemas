from django.urls import path
<<<<<<< Updated upstream
from loja.views import *

urlpatterns = [
    path('', ListarLojas.as_view(), name='listar-lojas'),
     path('novo/', CriarLoja.as_view(), name='criar-loja'),
    path('fotos/<str:arquivo>/', FotoLoja.as_view(), name='foto-loja')
=======
from .views import *

# Adiciona um namespace para o app 'loja'
app_name = 'loja'

urlpatterns = [
    path('', ListarLojas.as_view(), name='loja_list'),
    path('novo/', CriarLoja.as_view(), name='loja_create'),
    path('<int:pk>/', LojaDetailView.as_view(), name='loja_detail'),
>>>>>>> Stashed changes
]