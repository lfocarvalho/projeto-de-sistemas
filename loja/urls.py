from django.urls import path
from .views import *

# Adiciona um namespace para o app 'loja'
app_name = 'loja'

urlpatterns = [
    path('', ListarLojas.as_view(), name='loja_list'),
    path('novo/', CriarLoja.as_view(), name='loja_create'),
    path('<int:pk>/', LojaDetailView.as_view(), name='loja_detail'),
]