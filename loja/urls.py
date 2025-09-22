from django.urls import path
from loja.views import *

urlpatterns = [
    path('', ListarLojas.as_view(), name='listar-lojas')
]