from django.utils import timezone
from django import forms
from .models import Agendamento
from produto.models import Produto, Categoria

class AgendamentoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        loja_id = kwargs.pop('loja_id', None)
        super().__init__(*args, **kwargs)
        self.fields['produto'].queryset = Produto.objects.none()
        if loja_id:
            try:
                # Filtra os produtos para mostrar apenas os que são da categoria 'Serviços'
                categoria_servicos = Categoria.objects.get(nome='Serviço')
                self.fields['produto'].queryset = Produto.objects.filter(
                    loja_id=loja_id,
                    disponivel=True,
                    categoria=categoria_servicos
                ).order_by('nome')
            except Categoria.DoesNotExist:
                # Se a categoria 'Serviços' não existir, o queryset continua vazio.
                pass

        # Melhora a experiência do usuário se não houver serviços
        if not self.fields['produto'].queryset.exists():
            self.fields['produto'].empty_label = "Nenhum serviço disponível para agendamento."
            self.fields['produto'].disabled = True

    class Meta:
        model = Agendamento
        fields = ['produto', 'data_hora', 'observacoes']
        widgets = {
            'data_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'produto': forms.Select(attrs={'class': 'form-select'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ex: Meu pet é alérgico a...'}),
        }
    def clean_data_hora(self):
        data_hora = self.cleaned_data.get('data_hora')
        if data_hora and data_hora < timezone.now():
            raise forms.ValidationError("A data e hora do agendamento não podem ser no passado.")
        return data_hora