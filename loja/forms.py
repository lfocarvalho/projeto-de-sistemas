from django.forms import ModelForm
from loja.models import Loja

class FormularioLoja(ModelForm):
    """
    Formulário para o model Veículo
    """

    class Meta:
        model = Loja
        exclude = []