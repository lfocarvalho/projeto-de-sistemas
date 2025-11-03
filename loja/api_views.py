import math
from django.http import JsonResponse
from .models import Loja

# Função auxiliar para calcular a distância Haversine entre dois pontos
# Retorna a distância em quilômetros
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Raio da Terra em quilômetros

    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad

    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def listar_lojas_api(request):
    lojas_data = []
    user_lat_str = request.GET.get('lat')
    user_lon_str = request.GET.get('lon')

    # Filtra apenas lojas que possuem latitude e longitude cadastradas
    lojas = Loja.objects.filter(latitude__isnull=False, longitude__isnull=False)

    user_lat = None
    user_lon = None
    if user_lat_str and user_lon_str:
        try:
            user_lat = float(user_lat_str)
            user_lon = float(user_lon_str)
        except (ValueError, TypeError):
            pass

    for loja in lojas:
        distancia = None
        if user_lat is not None and user_lon is not None:
            distancia = haversine_distance(user_lat, user_lon, float(loja.latitude), float(loja.longitude))
            distancia = round(distancia, 2)

        lojas_data.append({
            'id': loja.id,
            'nome': loja.nome,
            'endereco': loja.endereco,
            'latitude': float(loja.latitude),
            'longitude': float(loja.longitude),
            'distancia': distancia
        })
    
    if user_lat is not None and user_lon is not None:
        lojas_data.sort(key=lambda x: x['distancia'] if x['distancia'] is not None else float('inf'))

    return JsonResponse(lojas_data, safe=False)