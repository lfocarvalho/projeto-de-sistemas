from .models import Loja, CarouselImage

def loja_context(request):
    """
    Torna a variável 'is_store_user' global para o template.
    """
    is_store_user = False
    if request.user.is_authenticated:
        # Verifica se o usuário logado tem uma loja associada ao seu e-mail
        is_store_user = Loja.objects.filter(email=request.user.email).exists()

    return {
        'is_store_user': is_store_user
    }

def carousel_context(request):
    """
    Torna as imagens do carrossel globais para o template (para o base.html).
    """
    carousel_images = CarouselImage.objects.all().order_by('order')
    return {
        'carousel_images': carousel_images
    }