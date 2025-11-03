from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, UpdateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Avg, Count

from loja.models import Loja
from produto.models import Produto
from loja.forms import FormularioLoja # Reutilizando seu formulário de loja


class LojistaRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin que verifica se o usuário é um lojista (baseado no e-mail).
    Redireciona para o login se não estiver logado ou para a home se não for lojista.
    """
    login_url = reverse_lazy('login')
    
    def test_func(self):
        # Verifica se o usuário é superadmin OU se tem uma loja associada ao seu e-mail
        if self.request.user.is_superuser:
            return True
        return Loja.objects.filter(email=self.request.user.email).exists()
    
    def handle_no_permission(self):
        # Se não for lojista, mas estiver logado, redireciona para a home
        if self.request.user.is_authenticated:
            return redirect('loja:loja_list') 
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        # Adiciona a loja do usuário ao contexto de todas as views do painel
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_superuser:
            context['loja_usuario'] = get_object_or_404(Loja, email=self.request.user.email)
        # Para superusuários, 'loja_usuario' será None (eles não têm uma loja)
        return context


class DashboardHomeView(LojistaRequiredMixin, TemplateView):
    """
    Página inicial do dashboard do lojista.
    """
    template_name = 'painel_lojista/dashboard_home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Meu Painel'
        
        try:
            # Pega a loja (seja do contexto ou buscando de novo para o superuser)
            if self.request.user.is_superuser:
                # Superuser vê estatísticas de todas as lojas
                context['total_produtos'] = Produto.objects.count()
                context['total_lojas'] = Loja.objects.count()
                context['media_geral_avaliacoes'] = Loja.objects.aggregate(media=Avg('avaliacao_media'))['media']
                context['is_admin_dashboard'] = True
            else:
                loja = context['loja_usuario']
                produtos = Produto.objects.filter(loja=loja)
                context['total_produtos'] = produtos.count()
                context['media_avaliacoes_produtos'] = produtos.aggregate(media=Avg('avaliacao_media'))['media']
                context['produtos_recentes'] = produtos.order_by('-id')[:5] # 5 produtos mais recentes
        
        except Loja.DoesNotExist:
            # Isso não deve acontecer por causa do LojistaRequiredMixin, mas é uma garantia
            context['total_produtos'] = 0

        return context


class MinhaLojaUpdateView(LojistaRequiredMixin, UpdateView):
    """
    View para o lojista editar as informações da sua própria loja.
    """
    model = Loja
    form_class = FormularioLoja
    template_name = 'loja/novo.html' # Reutilizando seu template de formulário
    success_url = reverse_lazy('painel_lojista:dashboard_home')

    def get_object(self, queryset=None):
        """ Garante que o usuário só possa editar sua própria loja. """
        # Superusuários podem editar qualquer loja (pelo ID na URL)
        if self.request.user.is_superuser:
            pk = self.kwargs.get('pk')
            if pk:
                return get_object_or_404(Loja, pk=pk)
            # Se superuser acessar sem pk, não faz sentido.
            raise Http404("Superusuário deve especificar o PK da loja.")
            
        # Lojistas normais só podem editar a loja associada ao seu e-mail
        return get_object_or_404(Loja, email=self.request.user.email)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f'Editar Minha Loja: {self.object.nome}'
        return context


class MeusProdutosListView(LojistaRequiredMixin, ListView):
    """
    View para o lojista ver e gerenciar todos os seus produtos.
    """
    model = Produto
    template_name = 'painel_lojista/meus_produtos_list.html'
    context_object_name = 'produtos'
    paginate_by = 10

    def get_queryset(self):
        """ Filtra a lista para mostrar apenas produtos da loja do usuário. """
        if self.request.user.is_superuser:
            # Superusuário vê todos os produtos
            return Produto.objects.all().select_related('loja', 'categoria').order_by('-id')
        
        # Lojista normal vê apenas seus produtos
        return Produto.objects.filter(loja__email=self.request.user.email).select_related('categoria').order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Meus Produtos'
        return context