from django.urls import path
from . import views
from .api import SalvarLocalizacaoLojaView, api_listar_lojas

app_name = 'loja'

urlpatterns = [
   path('', views.ListarLojas.as_view(), name='loja_list'),
    path('novo/', views.CriarLoja.as_view(), name='loja_create'),
    path('<int:pk>/', views.LojaDetailView.as_view(), name='loja_detail'),
    path('<int:loja_id>/avaliar/', views.avaliar_loja, name='avaliar-loja'),
    path('<int:loja_id>/favoritar/', views.favoritar_loja, name='favoritar-loja'),
    path('mapa/', views.mapa_lojas_view, name='mapa_view'),
    path('perfil/', views.perfil_usuario, name='perfil_usuario'),

    # Rota da API
    path('api/lojas/', api_listar_lojas, name='api-listar-lojas'),
    path('api/loja/<int:loja_id>/salvar-localizacao/', SalvarLocalizacaoLojaView.as_view(), name='api-salvar-localizacao'),
]