from django import forms
from loja.models import Loja

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