from django.http import JsonResponse
from .models import Loja
from django.db.models import Q
from django.db.models import F
from django.db.models.functions import Sin, Cos, Radians, ACos

def listar_lojas_api(request):
    """
    API endpoint que retorna uma lista de lojas.
    Se lat/lon forem fornecidos, retorna as lojas ordenadas por distância.
    """
    user_lat = request.GET.get('lat')
    user_lon = request.GET.get('lon')

    # Filtra lojas que têm coordenadas e que não são 0.0
    lojas = Loja.objects.filter(
        latitude__isnull=False, longitude__isnull=False
    ).exclude(Q(latitude=0) & Q(longitude=0))

    if user_lat and user_lon:
        try:
            user_lat = float(user_lat)
            user_lon = float(user_lon)

            # Fórmula de Haversine para calcular a distância em uma esfera
            # 6371 é o raio da Terra em quilômetros.
            distancia = 6371 * ACos(
                Cos(Radians(user_lat)) * Cos(Radians(F('latitude'))) *
                Cos(Radians(F('longitude')) - Radians(user_lon)) +
                Sin(Radians(user_lat)) * Sin(Radians(F('latitude')))
            )
            
            lojas = lojas.annotate(
                distancia=distancia
            ).order_by('distancia')

        except (ValueError, TypeError):
            # Ignora lat/lon inválidos e continua sem ordenar por distância
            pass

    data = [
        {
            "id": loja.id,
            "nome": loja.nome,
            "endereco": loja.endereco,
            "latitude": loja.latitude,
            "longitude": loja.longitude,
            # Adiciona a distância ao JSON se ela foi calculada
            "distancia": round(loja.distancia, 2) if hasattr(loja, 'distancia') else None
        }
        for loja in lojas
    ]
    
    return JsonResponse(data, safe=False)
