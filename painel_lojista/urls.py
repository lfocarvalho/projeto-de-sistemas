from django.urls import path
from . import views

app_name = 'painel_lojista'

urlpatterns = [
    path('', views.DashboardHomeView.as_view(), name='dashboard_home'),
    path('minha-loja/editar/', views.MinhaLojaUpdateView.as_view(), name='minha_loja_update'),
    path('meus-produtos/', views.MeusProdutosListView.as_view(), name='meus_produtos_list'),
    
    # Rota para superusuários editarem lojas específicas pelo painel
    path('loja/<int:pk>/editar/', views.MinhaLojaUpdateView.as_view(), name='admin_loja_update'),
]