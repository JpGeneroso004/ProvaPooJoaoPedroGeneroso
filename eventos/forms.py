from django import forms
from django.db import models as django_models
from .models import Evento
from .fields import DataBRField
from inventario.models import Tenda, ConjuntoPalco


class EventoForm(forms.ModelForm):
    tendas = forms.ModelMultipleChoiceField(
        queryset=Tenda.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='Tendas'
    )
    conjuntos = forms.ModelMultipleChoiceField(
        queryset=ConjuntoPalco.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='Conjuntos de Palco/Piso'
    )
    data_inicio = DataBRField(label='Data de Início')
    data_fim    = DataBRField(label='Data de Fim')

    class Meta:
        model = Evento
        fields = ['nome', 'cliente', 'telefone', 'local', 'cidade',
                  'latitude', 'longitude', 'data_inicio', 'data_fim',
                  'status', 'observacoes', 'tendas', 'conjuntos']
        widgets = {
            'nome':      forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do evento'}),
            'cliente':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do cliente'}),
            'telefone':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': '(61) 99999-9999'}),
            'local':     forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Endereço completo'}),
            'cidade':    forms.TextInput(attrs={'class': 'form-control'}),
            'latitude':  forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001', 'placeholder': 'Ex: -15.5438'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.0000001', 'placeholder': 'Ex: -47.3344'}),
            'status':      forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super().__init__(*args, **kwargs)
        if instance and instance.pk:
            self.fields['tendas'].queryset = Tenda.objects.filter(
                django_models.Q(status='disponivel') | django_models.Q(eventos=instance)
            ).distinct().order_by('tamanho', 'tipo', 'codigo')
            self.fields['conjuntos'].queryset = ConjuntoPalco.objects.filter(
                django_models.Q(status='disponivel') | django_models.Q(eventos=instance)
            ).distinct()
        else:
            self.fields['tendas'].queryset = Tenda.objects.filter(
                status='disponivel').order_by('tamanho', 'tipo', 'codigo')
            self.fields['conjuntos'].queryset = ConjuntoPalco.objects.filter(
                status='disponivel')

    def clean(self):
        cleaned_data = super().clean()
        data_inicio = cleaned_data.get('data_inicio')
        data_fim    = cleaned_data.get('data_fim')
        if data_inicio and data_fim and data_fim < data_inicio:
            self.add_error('data_fim', 'A data de fim não pode ser anterior à data de início.')
        return cleaned_data
