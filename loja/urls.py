from django.urls import path
from loja.views import *

urlpatterns = [
    path('', ListarLojas.as_view(), name='listar-lojas'),
     path('novo/', CriarLoja.as_view(), name='criar-loja'),
    path('fotos/<str:arquivo>/', FotoLoja.as_view(), name='foto-loja')
]