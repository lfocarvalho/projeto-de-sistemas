from datetime import timezone
from django import forms
from .models import Agendamento
from produto.models import Produto

class AgendamentoForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        loja_id = kwargs.pop('loja_id', None)
        super(AgendamentoForm, self).__init__(*args, **kwargs)
        
        if loja_id:
            self.fields['produto'].queryset = Produto.objects.filter(
                loja_id=loja_id, 
                disponivel=True
            )

    class Meta:
        model = Agendamento
        fields = ['produto', 'data_hora', 'observacoes']
        
        widgets = {
            'data_hora': forms.DateTimeInput(
                attrs={'type': 'datetime-local', 'class': 'form-control'},
                format='%Y-%m-%dT%H:%M'
            ),
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
    def clean_data_hora(self):
        data_hora = self.cleaned_data.get('data_hora')
        if data_hora and data_hora < timezone.now():
            raise forms.ValidationError("A data e hora do agendamento não podem ser no passado.")
        return data_hora
    def clean_data_hora(self):
        data_hora = self.cleaned_data.get('data_hora')
        return data_hora