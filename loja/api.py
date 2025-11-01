from django.http import JsonResponse, HttpResponseBadRequest
from django.views import View
from django.db.models.functions import Radians, Sin, Cos, Sqrt, ATan2
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Loja
import json

def api_listar_lojas(request):
    """
    API para listar lojas, opcionalmente ordenadas por proximidade.
    """
    lat = request.GET.get('lat')
    lon = request.GET.get('lon')
    lojas = Loja.objects.all()

    if lat and lon:
        try:
            user_lat = Radians(float(lat))
            user_lon = Radians(float(lon))
            lojas = lojas.annotate(
                dlat=Radians('latitude') - user_lat,
                dlon=Radians('longitude') - user_lon
            ).annotate(
                a=Sin('dlat' / 2)**2 + Cos(user_lat) * Cos(Radians('latitude')) * Sin('dlon' / 2)**2
            ).annotate(
                c=2 * ATan2(Sqrt('a'), Sqrt(1 - 'a'))
            ).annotate(
                distancia=6371 * 'c'  # Raio da Terra em km
            ).order_by('distancia')
        except (ValueError, TypeError):
            lojas = lojas.order_by('nome')
    else:
        lojas = lojas.order_by('nome')

    lojas_data = []
    for loja in lojas:
        loja_dict = {
            'id': loja.id, 
            'nome': loja.nome, 
            'endereco': loja.endereco, 
            'latitude': loja.latitude, 
            'longitude': loja.longitude,
            'atendimento_emergencia': loja.atendimento_emergencia  # Adicionando o campo
        }
        if lat and lon and hasattr(loja, 'distancia'):
            loja_dict['distancia'] = round(loja.distancia, 2) if loja.distancia is not None else None
        lojas_data.append(loja_dict)

    data = lojas_data
    return JsonResponse(data, safe=False)


class SalvarLocalizacaoLojaView(UserPassesTestMixin, View):
    """
    API para que um superusuário salve a localização de uma loja.
    """
    def test_func(self):
        return self.request.user.is_superuser

    def post(self, request, loja_id):
        loja = Loja.objects.get(pk=loja_id)
        data = json.loads(request.body)
        loja.latitude = data.get('lat')
        loja.longitude = data.get('lon')
        loja.save()
        return JsonResponse({'success': True, 'message': 'Localização atualizada com sucesso!'})