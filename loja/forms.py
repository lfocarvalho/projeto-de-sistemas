from django import forms
from loja.models import Loja
from loja.models import Avaliacao

class FormularioLoja(forms.ModelForm):
    """
    Formulário para o model Loja.
    """

    class Meta:
        model = Loja
        fields = [
            'nome', 'endereco', 'descricao', 'telefone', 
            'horario_abertura', 'horario_fechamento', 'atendimento_emergencia',
            'email', 'website', 'foto'
        ]
        widgets = {
            'horario_abertura': forms.TimeInput(attrs={'type': 'time'}),
            'horario_fechamento': forms.TimeInput(attrs={'type': 'time'}),
        }


class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
        widgets = {
            'nota': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
