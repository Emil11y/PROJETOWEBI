from django import forms
from django.db.models import Q
from django.core.exceptions import ValidationError
from .models import Veiculo, Cliente,Locacao, Funcionario
from .models import Funcionario, Agencia, Acessorio, Pagamento, HistoricoQuilometragem, VeiculoAcessorio, Manutencao
class VeiculoForm(forms.ModelForm):
    class Meta:
        model = Veiculo
        fields = '__all__'

class ClienteForm(forms.ModelForm): 
    class Meta:
        model = Cliente
        fields = '__all__'
        
#  LocacaoForm
class LocacaoForm(forms.ModelForm):
    class Meta:
        model = Locacao
        fields = '__all__' 
        widgets = {
            'data_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'), # DateTimeInput para data e hora
            'data_fim_prevista': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'data_fim_real': forms.DateTimeInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'valor_total': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Cliente.objects.order_by('nome')
        
        if self.instance and self.instance.pk: 
            self.fields['veiculo'].queryset = Veiculo.objects.filter(Q(status_disponibilidade='Disponível') | Q(pk=self.instance.veiculo.pk)).order_by('modelo')
        else: 
            self.fields['veiculo'].queryset = Veiculo.objects.filter(status_disponibilidade='Disponível').order_by('modelo')
        
        self.fields['cliente'].queryset = Cliente.objects.order_by('nome')
        self.fields['veiculo'].queryset = Veiculo.objects.filter(status_disponibilidade='Disponível').order_by('modelo')
       
        self.fields['funcionario'].queryset = Funcionario.objects.order_by('nome')
        self.fields['agencia'].queryset = Agencia.objects.order_by('nome_agencia')


        self.fields['data_fim_real'].required = False
        self.fields['valor_total'].required = False 

    def clean(self):
        cleaned_data = super().clean() 

        data_inicio = cleaned_data.get('data_inicio')
        data_fim_prevista = cleaned_data.get('data_fim_prevista')
        veiculo = cleaned_data.get('veiculo')

        
        if data_inicio and data_fim_prevista and veiculo:
            
            if data_fim_prevista < data_inicio:
                raise ValidationError("A 'Data fim prevista' não pode ser anterior à 'Data início'.")

           
            conflitos = Locacao.objects.filter(
                veiculo=veiculo, # Para o mesmo veículo
                data_inicio__lt=data_fim_prevista, # Conflito começa antes do fim da nova locação
                data_fim_prevista__gt=data_inicio # E termina depois do início da nova locação
            )

           
            if self.instance and self.instance.pk:
                conflitos = conflitos.exclude(pk=self.instance.pk)

            if conflitos.exists():
                raise ValidationError(
                    f"Este veículo já está reservado ou alugado no período selecionado. "
                    f"Conflito com a locação ID: {conflitos.first().id_locacao} (de {conflitos.first().data_inicio.strftime('%d/%m/%Y')} a {conflitos.first().data_fim_prevista.strftime('%d/%m/%Y')})."
                )

        return cleaned_data 



#  FuncionarioForm
class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = '__all__' 
        widgets = {
            'data_contratacao': forms.DateInput(attrs={'type': 'date'}),
        }

#AgenciaForm
class AgenciaForm(forms.ModelForm):
    class Meta:
        model = Agencia
        fields = '__all__'

# AcessorioForm
class AcessorioForm(forms.ModelForm):
    class Meta:
        model = Acessorio
        fields = '__all__'

# PagamentoForm
class PagamentoForm(forms.ModelForm):
    class Meta:
        model = Pagamento
        fields = '__all__' 
        widgets = {
           }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
        self.fields['locacao']

class HistoricoQuilometragemForm(forms.ModelForm): 
    class Meta:
        model = HistoricoQuilometragem
        fields = '__all__'
        widgets = {
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veiculo'].queryset = Veiculo.objects.all().order_by('modelo', 'placa')

class VeiculoAcessorioForm(forms.ModelForm):
    class Meta:
        model = VeiculoAcessorio
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['veiculo'].queryset = Veiculo.objects.all().order_by('modelo', 'placa')
        self.fields['acessorio'].queryset = Acessorio.objects.all().order_by('nome_acessorio')

class ManutencaoForm(forms.ModelForm): # <--- Confirme que o nome está EXATO
    class Meta:
        model = Manutencao
        fields = '__all__'
        widgets = {
            'data_inicio_manutencao': forms.DateInput(attrs={'type': 'date'}),
            'data_fim_manutencao': forms.DateInput(attrs={'type': 'date'}),
            'previsao': forms.Textarea(attrs={'rows': 3}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['veiculo'].queryset = Veiculo.objects.all().order_by('modelo', 'placa')
        self.fields['funcionario'].queryset = Funcionario.objects.all().order_by('nome')
        self.fields['data_fim_manutencao'].required = False
        self.fields['custo'].required = False