# core/models.py
from django.db import models
from datetime import timedelta

# 1. TipoVeiculo
class TipoVeiculo(models.Model):
    id_tipo_veiculo = models.AutoField(primary_key=True) # Assumindo que id é PK autoincrement
    nome_tipo = models.CharField(max_length=50)
    descricao = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Tipo de Veículo"
        verbose_name_plural = "Tipos de Veículos"

    def __str__(self):
        return self.nome_tipo

# 2. Veiculo
class Veiculo(models.Model):
    id_veiculo = models.AutoField(primary_key=True)
    placa = models.CharField(max_length=8, unique=True)
    marca = models.CharField(max_length=45)
    modelo = models.CharField(max_length=45)
    ano = models.IntegerField()
    cor = models.CharField(max_length=30)
    quilometragem = models.DecimalField(max_digits=10, decimal_places=2) # Pode ser IntegerField se for sempre km inteiros
    status_disponibilidade = models.CharField(max_length=20, default='Disponível')
    valor_diario = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_veiculo = models.ForeignKey(TipoVeiculo, on_delete=models.SET_NULL, null=True, related_name='veiculos')

    
    class Meta:
        verbose_name = "Veículo"
        verbose_name_plural = "Veículos"

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.placa})"

# 3. Cliente
class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True) # Formato "XXX.XXX.XXX-XX"
    data_nascimento = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)
    endereco = models.CharField(max_length=255)
    num_cnh = models.CharField(max_length=20, unique=True, null=True, blank=True)
    data_val_cnh = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    def __str__(self):
        return f"{self.nome} {self.sobrenome} ({self.cpf})"

# 4. Funcionario
class Funcionario(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    sobrenome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=14, unique=True)
    data_contratacao = models.DateField()
    cargo = models.CharField(max_length=50)
    salario = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"

    def __str__(self):
        return f"{self.nome} {self.sobrenome} ({self.cargo})"

# 5. Agencia
class Agencia(models.Model):
    id_agencia = models.AutoField(primary_key=True)
    nome_agencia = models.CharField(max_length=100)
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=50)
    telefone = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Agência"
        verbose_name_plural = "Agências"

    def __str__(self):
        return self.nome_agencia

# 6. Acessorio
class Acessorio(models.Model):
    id_acessorio = models.AutoField(primary_key=True)
    nome_acessorio = models.CharField(max_length=100)
    valor_diario = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Acessório"
        verbose_name_plural = "Acessórios"

    def __str__(self):
        return self.nome_acessorio

# 7. Locacao (depende de Cliente, Veiculo, Funcionario, Agencia)
class Locacao(models.Model):
    id_locacao = models.AutoField(primary_key=True)
    data_inicio = models.DateTimeField()
    data_fim_prevista = models.DateTimeField()
    data_fim_real = models.DateTimeField(null=True, blank=True)
    valor_total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status_locacao = models.CharField(max_length=20, default='Reservada') 

    cliente = models.ForeignKey(Cliente, on_delete=models.PROTECT, related_name='locacoes')
    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name='locacoes')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True, related_name='locacoes_atendidas')
    agencia = models.ForeignKey(Agencia, on_delete=models.PROTECT, related_name='locacoes_origem')

    class Meta:
        verbose_name = "Locação"
        verbose_name_plural = "Locações"

    def __str__(self):
        return f"Locação #{self.id_locacao} - {self.cliente.nome} - {self.veiculo.placa}"
    def save(self, *args, **kwargs):
       
        if self.data_inicio and self.data_fim_prevista:
            duracao_prevista: timedelta = self.data_fim_prevista - self.data_inicio
            num_dias = duracao_prevista.days
            if num_dias < 0: 
                 num_dias = 0
            
            if self.veiculo and self.veiculo.valor_diario is not None:
                self.valor_total = self.veiculo.valor_diario * num_dias
            # TODO: Futuramente, adicionar cálculo de acessórios aqui. Por enquanto, só o veículo.

        
        if self.veiculo:
            if self.pk is None: 
                if self.status_locacao in ['Reservada', 'Ativa']:
                    self.veiculo.status_disponibilidade = 'Alugado'
                    self.veiculo.save() 
            else: 
                original_locacao = Locacao.objects.get(pk=self.pk) 

                if original_locacao.status_locacao not in ['Finalizada', 'Cancelada'] and \
                   self.status_locacao in ['Finalizada', 'Cancelada']:
                    self.veiculo.status_disponibilidade = 'Disponível'
                    self.veiculo.save()
                
                elif original_locacao.status_locacao in ['Finalizada', 'Cancelada'] and \
                     self.status_locacao in ['Reservada', 'Ativa']:
                    self.veiculo.status_disponibilidade = 'Alugado'
                    self.veiculo.save()

        super().save(*args, **kwargs)

# 8. Pagamento (depende de Locacao)
class Pagamento(models.Model):
    id_pagamento = models.AutoField(primary_key=True)
    data_pagamento = models.DateTimeField(auto_now_add=True)
    valor_pago = models.DecimalField(max_digits=10, decimal_places=2)
    metodo_pagamento = models.CharField(max_length=50)
    status_pagamento = models.CharField(max_length=20, default='Pendente') # Ex: Pendente, Pago, Estornado
    observacoes = models.TextField(blank=True, null=True)

    locacao = models.ForeignKey(Locacao, on_delete=models.CASCADE, related_name='pagamentos') # CASCADE para deletar pagamentos se locação for deletada

    class Meta:
        verbose_name = "Pagamento"
        verbose_name_plural = "Pagamentos"

    def __str__(self):
        return f"Pagamento #{self.id_pagamento} - Locação #{self.locacao.id_locacao}"

# 9. VeiculoAcessorio (Tabela Associativa N:N com atributos, depende de Veiculo e Acessorio)
class VeiculoAcessorio(models.Model):
    id_veiculo_acessorio = models.AutoField(primary_key=True)
    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE)
    acessorio = models.ForeignKey(Acessorio, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1) # Quantidade daquele acessorio para aquele veiculo

    class Meta:
        verbose_name = "Acessório do Veículo"
        verbose_name_plural = "Acessórios dos Veículos"
        unique_together = ('veiculo', 'acessorio') # Garante que um par veiculo-acessorio é único

    def __str__(self):
        return f"{self.veiculo.placa} - {self.acessorio.nome_acessorio} ({self.quantidade})"

# 10. HistoricoQuilometragem (depende de Veiculo)
class HistoricoQuilometragem(models.Model):
    id_historico_quilometragem = models.AutoField(primary_key=True)
    data_registro = models.DateTimeField(auto_now_add=True)
    quilometragem_registrada = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True, null=True)

    veiculo = models.ForeignKey(Veiculo, on_delete=models.CASCADE, related_name='historico_quilometragem')

    class Meta:
        verbose_name = "Histórico de Quilometragem"
        verbose_name_plural = "Históricos de Quilometragem"

    def __str__(self):
        return f"KM: {self.quilometragem_registrada} em {self.data_registro.strftime('%d/%m/%Y %H:%M')}"

# 11. Manutencao (depende de Veiculo e Funcionario)
class Manutencao(models.Model):
    id_manutencao = models.AutoField(primary_key=True)
    data_inicio_manutencao = models.DateField()
    data_fim_manutencao = models.DateField(null=True, blank=True)
    previsao = models.TextField(blank=True, null=True) # Descrição da previsão do serviço
    custo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    tipo_manutencao = models.CharField(max_length=50) # Ex: Preventiva, Corretiva, Pneu
    observacoes = models.TextField(blank=True, null=True)

    veiculo = models.ForeignKey(Veiculo, on_delete=models.PROTECT, related_name='manutencoes')
    funcionario = models.ForeignKey(Funcionario, on_delete=models.SET_NULL, null=True, blank=True, related_name='manutencoes_responsavel')

    class Meta:
        verbose_name = "Manutenção"
        verbose_name_plural = "Manutenções"

    def __str__(self):
        return f"Manutenção: {self.tipo_manutencao} - Veículo: {self.veiculo.placa}"

