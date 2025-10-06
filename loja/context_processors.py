from .models import CarouselImage

def carousel_context(request):
    """
    Disponibiliza as imagens do carrossel para todos os templates.
    """
    return {'carousel_images': CarouselImage.objects.all()}