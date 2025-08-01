# Generated by Django 5.2.3 on 2025-06-21 01:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acessorio',
            fields=[
                ('id_acessorio', models.AutoField(primary_key=True, serialize=False)),
                ('nome_acessorio', models.CharField(max_length=100)),
                ('valor_diario', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'verbose_name': 'Acessório',
                'verbose_name_plural': 'Acessórios',
            },
        ),
        migrations.CreateModel(
            name='Agencia',
            fields=[
                ('id_agencia', models.AutoField(primary_key=True, serialize=False)),
                ('nome_agencia', models.CharField(max_length=100)),
                ('endereco', models.CharField(max_length=255)),
                ('cidade', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=50)),
                ('telefone', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Agência',
                'verbose_name_plural': 'Agências',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id_cliente', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('sobrenome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('data_nascimento', models.DateField(blank=True, null=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefone', models.CharField(max_length=20)),
                ('endereco', models.CharField(max_length=255)),
                ('num_cnh', models.CharField(blank=True, max_length=20, null=True, unique=True)),
                ('data_val_cnh', models.DateField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Funcionario',
            fields=[
                ('id_funcionario', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('sobrenome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=14, unique=True)),
                ('data_contratacao', models.DateField()),
                ('cargo', models.CharField(max_length=50)),
                ('salario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('telefone', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Funcionário',
                'verbose_name_plural': 'Funcionários',
            },
        ),
        migrations.CreateModel(
            name='TipoVeiculo',
            fields=[
                ('id_tipo_veiculo', models.AutoField(primary_key=True, serialize=False)),
                ('nome_tipo', models.CharField(max_length=50)),
                ('descricao', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Tipo de Veículo',
                'verbose_name_plural': 'Tipos de Veículos',
            },
        ),
        migrations.CreateModel(
            name='Locacao',
            fields=[
                ('id_locacao', models.AutoField(primary_key=True, serialize=False)),
                ('data_inicio', models.DateTimeField()),
                ('data_fim_prevista', models.DateTimeField()),
                ('data_fim_real', models.DateTimeField(blank=True, null=True)),
                ('valor_total', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('status_locacao', models.CharField(default='Reservada', max_length=20)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('agencia', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='locacoes_origem', to='core.agencia')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='locacoes', to='core.cliente')),
                ('funcionario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='locacoes_atendidas', to='core.funcionario')),
            ],
            options={
                'verbose_name': 'Locação',
                'verbose_name_plural': 'Locações',
            },
        ),
        migrations.CreateModel(
            name='Pagamento',
            fields=[
                ('id_pagamento', models.AutoField(primary_key=True, serialize=False)),
                ('data_pagamento', models.DateTimeField(auto_now_add=True)),
                ('valor_pago', models.DecimalField(decimal_places=2, max_digits=10)),
                ('metodo_pagamento', models.CharField(max_length=50)),
                ('status_pagamento', models.CharField(default='Pendente', max_length=20)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('locacao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pagamentos', to='core.locacao')),
            ],
            options={
                'verbose_name': 'Pagamento',
                'verbose_name_plural': 'Pagamentos',
            },
        ),
        migrations.CreateModel(
            name='Veiculo',
            fields=[
                ('id_veiculo', models.AutoField(primary_key=True, serialize=False)),
                ('placa', models.CharField(max_length=8, unique=True)),
                ('marca', models.CharField(max_length=45)),
                ('modelo', models.CharField(max_length=45)),
                ('ano', models.IntegerField()),
                ('cor', models.CharField(max_length=30)),
                ('quilometragem', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status_disponibilidade', models.CharField(default='Disponível', max_length=20)),
                ('valor_diario', models.DecimalField(decimal_places=2, max_digits=10)),
                ('tipo_veiculo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='veiculos', to='core.tipoveiculo')),
            ],
            options={
                'verbose_name': 'Veículo',
                'verbose_name_plural': 'Veículos',
            },
        ),
        migrations.CreateModel(
            name='Manutencao',
            fields=[
                ('id_manutencao', models.AutoField(primary_key=True, serialize=False)),
                ('data_inicio_manutencao', models.DateField()),
                ('data_fim_manutencao', models.DateField(blank=True, null=True)),
                ('previsao', models.TextField(blank=True, null=True)),
                ('custo', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tipo_manutencao', models.CharField(max_length=50)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('funcionario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='manutencoes_responsavel', to='core.funcionario')),
                ('veiculo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='manutencoes', to='core.veiculo')),
            ],
            options={
                'verbose_name': 'Manutenção',
                'verbose_name_plural': 'Manutenções',
            },
        ),
        migrations.AddField(
            model_name='locacao',
            name='veiculo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='locacoes', to='core.veiculo'),
        ),
        migrations.CreateModel(
            name='HistoricoQuilometragem',
            fields=[
                ('id_historico_quilometragem', models.AutoField(primary_key=True, serialize=False)),
                ('data_registro', models.DateTimeField(auto_now_add=True)),
                ('quilometragem_registrada', models.DecimalField(decimal_places=2, max_digits=10)),
                ('observacoes', models.TextField(blank=True, null=True)),
                ('veiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='historico_quilometragem', to='core.veiculo')),
            ],
            options={
                'verbose_name': 'Histórico de Quilometragem',
                'verbose_name_plural': 'Históricos de Quilometragem',
            },
        ),
        migrations.CreateModel(
            name='VeiculoAcessorio',
            fields=[
                ('id_veiculo_acessorio', models.AutoField(primary_key=True, serialize=False)),
                ('quantidade', models.IntegerField(default=1)),
                ('acessorio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.acessorio')),
                ('veiculo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.veiculo')),
            ],
            options={
                'verbose_name': 'Acessório do Veículo',
                'verbose_name_plural': 'Acessórios dos Veículos',
                'unique_together': {('veiculo', 'acessorio')},
            },
        ),
    ]
