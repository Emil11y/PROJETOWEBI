from django.shortcuts import render, get_object_or_404, redirect
from .models import Veiculo, Cliente, Locacao, Funcionario, Agencia, Acessorio, Pagamento, HistoricoQuilometragem, VeiculoAcessorio, Manutencao
from .forms import VeiculoForm, ClienteForm, LocacaoForm, FuncionarioForm, AgenciaForm, AcessorioForm, PagamentoForm, HistoricoQuilometragemForm, VeiculoAcessorioForm, ManutencaoForm
from django.contrib import messages
from django.db.models import Q
from django.db.models import Count,Sum, F
from django.db.models.functions import ExtractMonth, ExtractYear
from datetime import datetime
from django.contrib.auth.decorators import login_required

def home(request):
    total_veiculos = Veiculo.objects.count()
    veiculos_disponiveis = Veiculo.objects.filter(status_disponibilidade='Disponível').count()
    veiculos_alugados = Veiculo.objects.filter(status_disponibilidade='Alugado').count()
    total_clientes = Cliente.objects.count()
    total_locacoes = Locacao.objects.count()
    total_funcionarios = Funcionario.objects.count()
    total_agencias = Agencia.objects.count()

   
    hoje = datetime.now()
    locacoes_ativas = Locacao.objects.filter(
        data_inicio__lte=hoje,
        data_fim_prevista__gte=hoje, 
        status_locacao='Ativa' 
    ).count()

   
    pagamentos_pendentes = Pagamento.objects.filter(status_pagamento='Pendente').count()

    
    mes_atual = hoje.month
    ano_atual = hoje.year
    
    faturamento_mes_atual_qs = Locacao.objects.filter(
        data_fim_real__year=ano_atual,
        data_fim_real__month=mes_atual,
        valor_total__isnull=False
    ).aggregate(total=Sum('valor_total'))['total'] or 0


    context = {
        'total_veiculos': total_veiculos,
        'veiculos_disponiveis': veiculos_disponiveis,
        'veiculos_alugados': veiculos_alugados,
        'total_clientes': total_clientes,
        'total_locacoes': total_locacoes,
        'locacoes_ativas': locacoes_ativas,
        'total_funcionarios': total_funcionarios,
        'total_agencias': total_agencias,
        'pagamentos_pendentes': pagamentos_pendentes,
        'faturamento_mes_atual': faturamento_mes_atual_qs,
    }
    return render(request, 'core/home.html', {'titulo': 'Bem-vindo à Locadora de Veículos!'})
@login_required
def lista_veiculos(request):
    query = request.GET.get('q')
    veiculos = Veiculo.objects.all().order_by('modelo')
    if query: 
       
        veiculos = veiculos.filter(
            Q(placa__icontains=query) |
            Q(marca__icontains=query) |
            Q(modelo__icontains=query)
        )
        messages.info(request, f"Exibindo resultados para '{query}'.")
    return render(request, 'core/lista_veiculos.html', {'veiculos': veiculos, 'query':query})

def detalhes_veiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    return render(request, 'core/detalhes_veiculo.html', {'veiculo': veiculo})

def adicionar_veiculo(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo adicionado com sucesso!')
            return redirect('lista_veiculos') 
        else:
            messages.error(request, 'Erro ao adicionar veículo. Verifique os campos.')
    else:
        form = VeiculoForm()
    return render(request, 'core/adicionar_veiculo.html', {'form': form})

def editar_veiculo(request, pk):
    veiculo = get_object_or_404(Veiculo, pk=pk)
    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Veículo atualizado com sucesso!')
            return redirect('detalhes_veiculo', pk=veiculo.pk) 
        else:
            messages.error(request, 'Erro ao atualizar veículo. Verifique os campos.')
    else:
        form = VeiculoForm(instance=veiculo)
    return render(request, 'core/editar_veiculo.html', {'form': form, 'veiculo': veiculo})

def excluir_veiculo(request, pk):
     veiculo = get_object_or_404(Veiculo, pk=pk)
     if request.method == 'POST':
         try: 
              veiculo.delete()
              messages.success(request, 'Veículo excluído com sucesso!')
              return redirect('lista_veiculos')
         except Exception as e:
            messages.error(request, f'Não foi possível excluir o veículo. Erro: {e}') 
            return redirect('detalhes_veiculo', pk=veiculo.pk)
     return render(request, 'core/excluir_veiculo.html', {'veiculo': veiculo})

def lista_clientes(request):
    query=request.GET.get('q')
    clientes = Cliente.objects.all().order_by('nome')
    if query:
        clientes =clientes.filter(
            Q(nome__icontains=query)|
            Q(sobrenome__icontains=query)|
            Q(cpf__icontains=query)|
            Q(email__icontains=query)
        )
    messages.info(request, f"Exibindo resultados para '{query}'.")
    return render(request, 'core/lista_clientes.html', {'clientes': clientes})

def detalhes_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'core/detalhes_cliente.html', {'cliente': cliente})

def adicionar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente adicionado com sucesso!')
            return redirect('lista_clientes')
        else:
            messages.error(request, 'Erro ao adicionar cliente. Verifique os campos.')
    else:
        form = ClienteForm()
    return render(request, 'core/adicionar_cliente.html', {'form': form})

def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente atualizado com sucesso!')
            return redirect('detalhes_cliente', pk=cliente.pk)
        else:
            messages.error(request, 'Erro ao atualizar cliente. Verifique os campos.')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'core/editar_cliente.html', {'form': form, 'cliente': cliente})

def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        try:
            cliente.delete()
            messages.success(request, 'Cliente excluído com sucesso!')
            return redirect('lista_clientes')
        except Exception as e:
            messages.error(request, f'Não foi possível excluir o cliente. Erro: {e}')
            return redirect('detalhes_cliente', pk=cliente.pk)
    return render(request, 'core/excluir_cliente.html', {'cliente': cliente})

# Views para Locações
def lista_locacoes(request):
    query = request.GET.get('q')
    locacoes = Locacao.objects.all().order_by('-data_inicio')
    if query:
        locacoes = locacoes.filter(
            Q(cliente__nome__icontains=query) |
            Q(cliente__sobrenome__icontains=query) |
            Q(veiculo__placa__icontains=query) |
            Q(veiculo__modelo__icontains=query) |
            Q(status_locacao__icontains=query)
        )
        messages.info(request, f"Exibindo resultados para '{query}'.")
    return render(request, 'core/lista_locacoes.html', {'locacoes': locacoes})

def detalhes_locacao(request, pk):
    locacao = get_object_or_404(Locacao, pk=pk)
    return render(request, 'core/detalhes_locacao.html', {'locacao': locacao})

def adicionar_locacao(request):
    if request.method == 'POST':
        form = LocacaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Locação adicionada com sucesso!')
            return redirect('lista_locacoes')
        else:
            messages.error(request, 'Erro ao adicionar locação. Verifique os campos.')
    else:
        form = LocacaoForm()
    return render(request, 'core/adicionar_locacao.html', {'form': form})

def editar_locacao(request, pk):
    locacao = get_object_or_404(Locacao, pk=pk)
    if request.method == 'POST':
        form = LocacaoForm(request.POST, instance=locacao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Locação atualizada com sucesso!')
            return redirect('detalhes_locacao', pk=locacao.pk)
        else:
            messages.error(request, 'Erro ao atualizar locação. Verifique os campos.')
    else:
        form = LocacaoForm(instance=locacao)
    return render(request, 'core/editar_locacao.html', {'form': form, 'locacao': locacao})

def excluir_locacao(request, pk):
    locacao = get_object_or_404(Locacao, pk=pk)
    if request.method == 'POST':
       try:
           locacao.delete()
           messages.success(request, 'Locação excluída com sucesso!')
           return redirect('lista_locacoes')
       except Exception as e:
           messages.error(request, f'Não foi possível excluir a locação. Erro: {e}')
           return redirect('detalhes_locacao', pk=locacao.pk)
    return render(request, 'core/excluir_locacao.html', {'locacao': locacao})

def lista_funcionarios(request):
    query = request.GET.get('q')
    funcionarios = Funcionario.objects.all().order_by('nome')
    if query:
        funcionarios = funcionarios.filter(
            Q(nome__icontains=query) |
            Q(sobrenome__icontains=query) |
            Q(cpf__icontains=query) |
            Q(cargo__icontains=query)
        )
        messages.info(request, f"Exibindo resultados para '{query}'.")
    return render(request, 'core/lista_funcionarios.html', {'funcionarios': funcionarios, 'query':query})

def detalhes_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    return render(request, 'core/detalhes_funcionario.html', {'funcionario': funcionario})

def adicionar_funcionario(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário adicionado com sucesso!')
            return redirect('lista_funcionarios')
        else:
            messages.error(request, 'Erro ao adicionar funcionário. Verifique os campos.')
    else:
        form = FuncionarioForm()
    return render(request, 'core/adicionar_funcionario.html', {'form': form})

def editar_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        form = FuncionarioForm(request.POST, instance=funcionario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Funcionário atualizado com sucesso!')
            return redirect('detalhes_funcionario', pk=funcionario.pk)
        else:
            messages.error(request, 'Erro ao atualizar funcionário. Verifique os campos.')
    else:
        form = FuncionarioForm(instance=funcionario)
    return render(request, 'core/editar_funcionario.html', {'form': form, 'funcionario': funcionario})

def excluir_funcionario(request, pk):
    funcionario = get_object_or_404(Funcionario, pk=pk)
    if request.method == 'POST':
        try:
            funcionario.delete()
            messages.success(request, 'Funcionário excluído com sucesso!')
            return redirect('lista_funcionarios')
        except Exception as e:
            messages.error(request, f'Não foi possível excluir o funcionário. Erro: {e}')
            return redirect('detalhes_funcionario', pk=funcionario.pk)
    return render(request, 'core/excluir_funcionario.html', {'funcionario': funcionario})

def lista_agencias(request):
    query = request.GET.get('q')
    agencias = Agencia.objects.all().order_by('nome_agencia')
    if query:
        agencias = agencias.filter(
            Q(nome_agencia__icontains=query) |
            Q(endereco__icontains=query) |
            Q(cidade__icontains=query)
        )
        messages.info(request, f"Exibindo resultados para '{query}'.")
    return render(request, 'core/lista_agencias.html', {'agencias': agencias, 'query':query})

def detalhes_agencia(request, pk):
    agencia = get_object_or_404(Agencia, pk=pk)
    return render(request, 'core/detalhes_agencia.html', {'agencia': agencia})

def adicionar_agencia(request):
    if request.method == 'POST':
        form = AgenciaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agência adicionada com sucesso!')
            return redirect('lista_agencias')
        else:
            messages.error(request, 'Erro ao adicionar agência. Verifique os campos.')
    else:
        form = AgenciaForm()
    return render(request, 'core/adicionar_agencia.html', {'form': form})

def editar_agencia(request, pk):
    agencia = get_object_or_404(Agencia, pk=pk)
    if request.method == 'POST':
        form = AgenciaForm(request.POST, instance=agencia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agência atualizada com sucesso!')
            return redirect('detalhes_agencia', pk=agencia.pk)
        else:
            messages.error(request, 'Erro ao atualizar agência. Verifique os campos.')
    else:
        form = AgenciaForm(instance=agencia)
    return render(request, 'core/editar_agencia.html', {'form': form, 'agencia': agencia})

def excluir_agencia(request, pk):
    agencia = get_object_or_404(Agencia, pk=pk)
    if request.method == 'POST':
        try:
            agencia.delete()
            messages.success(request, 'Agência excluída com sucesso!')
            return redirect('lista_agencias')
        except Exception as e:
            messages.error(request, f'Não foi possível excluir a agência. Erro: {e}')
            return redirect('detalhes_agencia', pk=agencia.pk)
    return render(request, 'core/excluir_agencia.html', {'agencia': agencia})

def lista_acessorios(request):
    query = request.GET.get('q')
    acessorios = Acessorio.objects.all().order_by('nome_acessorio')
    if query:
        acessorios = acessorios.filter(
            Q(nome_acessorio__icontains=query) | 
            Q(valor_diario__icontains=query)
        )
        messages.info(request, f"Exibindo resultados para '{query}'.")
    return render(request, 'core/lista_acessorios.html', {'acessorios': acessorios,  'query': query})

def detalhes_acessorio(request, pk):
    acessorio = get_object_or_404(Acessorio, pk=pk)
    return render(request, 'core/detalhes_acessorio.html', {'acessorio': acessorio})

def adicionar_acessorio(request):
    if request.method == 'POST':
        form = AcessorioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Acessório adicionado com sucesso!')
            return redirect('lista_acessorios')
        else:
            messages.error(request, 'Erro ao adicionar acessório. Verifique os campos.')
    else:
        form = AcessorioForm()
    return render(request, 'core/adicionar_acessorio.html', {'form': form})

def editar_acessorio(request, pk):
    acessorio = get_object_or_404(Acessorio, pk=pk)
    if request.method == 'POST':
        form = AcessorioForm(request.POST, instance=acessorio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Acessório atualizado com sucesso!')
            return redirect('detalhes_acessorio', pk=acessorio.pk)
        else:
            messages.error(request, 'Erro ao atualizar acessório. Verifique os campos.')
    else:
        form = AcessorioForm(instance=acessorio)
    return render(request, 'core/editar_acessorio.html', {'form': form, 'acessorio': acessorio})

def excluir_acessorio(request, pk):
    acessorio = get_object_or_404(Acessorio, pk=pk)
    if request.method == 'POST':
        try:
            acessorio.delete()
            messages.success(request, 'Acessório excluído com sucesso!')
            return redirect('lista_acessorios')
        except Exception as e:
            messages.error(request, f'Não foi possível excluir o acessório. Erro: {e}')
            return redirect('detalhes_acessorio', pk=acessorio.pk)
    return render(request, 'core/excluir_acessorio.html', {'acessorio': acessorio})

def lista_pagamentos(request):
    query = request.GET.get('q')
    pagamentos = Pagamento.objects.all().order_by('-data_pagamento') 
    if query:
        pagamentos = pagamentos.filter(
            Q(locacao__cliente__nome__icontains=query) |
            Q(locacao__cliente__sobrenome__icontains=query) |
            Q(locacao__veiculo__placa__icontains=query) |
            Q(locacao__veiculo__modelo__icontains=query) |
            Q(metodo_pagamento__icontains=query) |
            Q(valor_pago__icontains=query) 
        )
        messages.info(request, f"Exibindo resultados para '{query}'.")
    return render(request, 'core/lista_pagamentos.html', {'pagamentos': pagamentos,  'query': query})

def detalhes_pagamento(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    return render(request, 'core/detalhes_pagamento.html', {'pagamento': pagamento})

def adicionar_pagamento(request):
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pagamento adicionado com sucesso!')
            return redirect('lista_pagamentos')
        else:
            messages.error(request, 'Erro ao adicionar pagamento. Verifique os campos.')
    else:
        form = PagamentoForm()
    return render(request, 'core/adicionar_pagamento.html', {'form': form})

def editar_pagamento(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    if request.method == 'POST':
        form = PagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pagamento atualizado com sucesso!')
            return redirect('detalhes_pagamento', pk=pagamento.pk)
        else:
            messages.error(request, 'Erro ao atualizar pagamento. Verifique os campos.')
    else:
        form = PagamentoForm(instance=pagamento)
    return render(request, 'core/editar_pagamento.html', {'form': form, 'pagamento': pagamento})

def excluir_pagamento(request, pk):
    pagamento = get_object_or_404(Pagamento, pk=pk)
    if request.method == 'POST':
         try:
             pagamento.delete()
             messages.success(request, 'Pagamento excluído com sucesso!')
             return redirect('lista_pagamentos')
         except Exception as e:
             messages.error(request, f'Não foi possível excluir o pagamento. Erro: {e}')
             return redirect('detalhes_pagamento', pk=pagamento.pk)
    return render(request, 'core/excluir_pagamento.html', {'pagamento': pagamento})

def lista_historico_quilometragem(request):
    query = request.GET.get('q')
    historicos = HistoricoQuilometragem.objects.all().order_by('-data_registro')
    if query:
        historicos = historicos.filter(
            Q(veiculo__placa__icontains=query) |
            Q(veiculo__modelo__icontains=query) |
            Q(quilometragem_registrada__icontains=query)
        )
        messages.info(request, f"Exibindo resultados para '{query}'.")
    return render(request, 'core/lista_historico_quilometragem.html', {'historicos': historicos,  'query': query})

def detalhes_historico_quilometragem(request, pk):
    historico = get_object_or_404(HistoricoQuilometragem, pk=pk)
    return render(request, 'core/detalhes_historico_quilometragem.html', {'historico': historico})

def adicionar_historico_quilometragem(request):
    if request.method == 'POST':
        form = HistoricoQuilometragemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Histórico de quilometragem adicionado com sucesso!')
            return redirect('lista_historico_quilometragem')
        else:
            messages.error(request, 'Erro ao adicionar histórico de quilometragem. Verifique os campos.')
    else:
        form = HistoricoQuilometragemForm()
    return render(request, 'core/adicionar_historico_quilometragem.html', {'form': form})

def editar_historico_quilometragem(request, pk):
    historico = get_object_or_404(HistoricoQuilometragem, pk=pk)
    if request.method == 'POST':
        form = HistoricoQuilometragemForm(request.POST, instance=historico)
        if form.is_valid():
            form.save()
            messages.success(request, 'Histórico de quilometragem atualizado com sucesso!')
            return redirect('detalhes_historico_quilometragem', pk=historico.pk)
        else:
             messages.error(request, 'Erro ao atualizar histórico de quilometragem. Verifique os campos.')
    else:
       form = HistoricoQuilometragemForm(instance=historico)
    return render(request, 'core/editar_historico_quilometragem.html', {'form': form, 'historico': historico})

def excluir_historico_quilometragem(request, pk):
    historico = get_object_or_404(HistoricoQuilometragem, pk=pk)
    if request.method == 'POST':
        try:
            historico.delete()
            messages.success(request, 'Histórico de quilometragem excluído com sucesso!')
            return redirect('lista_historico_quilometragem')
        except Exception as e:
            messages.error(request, f'Não foi possível excluir o histórico de quilometragem. Erro: {e}')
            return redirect('detalhes_historico_quilometragem', pk=historico.pk)
    return render(request, 'core/excluir_historico_quilometragem.html', {'historico': historico})

def lista_veiculo_acessorios(request):
     query = request.GET.get('q')
     veiculo_acessorios = VeiculoAcessorio.objects.all().order_by('veiculo__modelo', 'acessorio__nome_acessorio')
     if query:
         veiculo_acessorios = veiculo_acessorios.filter(
            Q(veiculo__placa__icontains=query) |
            Q(veiculo__modelo__icontains=query) |
            Q(acessorio__nome__icontains=query)
        )
     messages.info(request, f"Exibindo resultados para '{query}'.")
     return render(request, 'core/lista_veiculo_acessorios.html', {'veiculo_acessorios': veiculo_acessorios, 'query': query})

def detalhes_veiculo_acessorio(request, pk):
    veiculo_acessorio = get_object_or_404(VeiculoAcessorio, pk=pk)
    return render(request, 'core/detalhes_veiculo_acessorio.html', {'veiculo_acessorio': veiculo_acessorio})

def adicionar_veiculo_acessorio(request):
    if request.method == 'POST':
        form = VeiculoAcessorioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Associação Veículo-Acessório adicionada com sucesso!')
            return redirect('lista_veiculo_acessorios')
        else:
            messages.error(request, 'Erro ao adicionar associação Veículo-Acessório. Verifique os campos.')
    else:
        form = VeiculoAcessorioForm()
    return render(request, 'core/adicionar_veiculo_acessorio.html', {'form': form})

def editar_veiculo_acessorio(request, pk):
    veiculo_acessorio = get_object_or_404(VeiculoAcessorio, pk=pk)
    if request.method == 'POST':
        form = VeiculoAcessorioForm(request.POST, instance=veiculo_acessorio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Associação Veículo-Acessório atualizada com sucesso!')
            return redirect('detalhes_veiculo_acessorio', pk=veiculo_acessorio.pk)
        else:
         messages.error(request, 'Erro ao atualizar associação Veículo-Acessório. Verifique os campos.')
    else:
        form = VeiculoAcessorioForm(instance=veiculo_acessorio)
    return render(request, 'core/editar_veiculo_acessorio.html', {'form': form, 'veiculo_acessorio': veiculo_acessorio})

def excluir_veiculo_acessorio(request, pk):
    veiculo_acessorio = get_object_or_404(VeiculoAcessorio, pk=pk)
    if request.method == 'POST':
        try:
           veiculo_acessorio.delete()
           messages.success(request, 'Associação Veículo-Acessório excluída com sucesso!')
           return redirect('lista_veiculo_acessorios')
        
        except Exception as e:
            messages.error(request, f'Não foi possível excluir a associação Veículo-Acessório. Erro: {e}')
            return redirect('detalhes_veiculo_acessorio', pk=veiculo_acessorio.pk)
    return render(request, 'core/excluir_veiculo_acessorio.html', {'veiculo_acessorio': veiculo_acessorio})

def lista_manutencoes(request): 
    query = request.GET.get('q')
    manutencoes = Manutencao.objects.all().order_by('-data_inicio_manutencao')
    if query:
        manutencoes = manutencoes.filter(
            Q(veiculo__placa__icontains=query) |
            Q(veiculo__modelo__icontains=query) |
            Q(funcionario__nome__icontains=query) |
            Q(funcionario__sobrenome__icontains=query) |
            Q(tipo_manutencao__icontains=query)
        )
        messages.info(request, f"Exibindo resultados para '{query}'.")
    return render(request, 'core/lista_manutencoes.html', {'manutencoes': manutencoes, 'query': query})

def detalhes_manutencao(request, pk):
    manutencao = get_object_or_404(Manutencao, pk=pk)
    return render(request, 'core/detalhes_manutencao.html', {'manutencao': manutencao})

def adicionar_manutencao(request):
    if request.method == 'POST':
        form = ManutencaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Manutenção atualizada com sucesso!')
            return redirect('lista_manutencoes')
        else:
            messages.error(request, 'Erro ao adicionar manutenção. Verifique os campos.')
    else:
        form = ManutencaoForm()
    return render(request, 'core/adicionar_manutencao.html', {'form': form})

def editar_manutencao(request, pk):
    manutencao = get_object_or_404(Manutencao, pk=pk)
    if request.method == 'POST':
        form = ManutencaoForm(request.POST, instance=manutencao)
        if form.is_valid():
            form.save()
            messages.success(request, 'Manutenção atualizada com sucesso!')
            return redirect('detalhes_manutencao', pk=manutencao.pk)
        else:
            messages.error(request, 'Erro ao atualizar manutenção. Verifique os campos.')
    else:
        form = ManutencaoForm(instance=manutencao)
    return render(request, 'core/editar_manutencao.html', {'form': form, 'manutencao': manutencao})

def excluir_manutencao(request, pk):
    manutencao = get_object_or_404(Manutencao, pk=pk)
    if request.method == 'POST':
        try: 
            manutencao.delete()
            messages.success(request, 'Manutenção excluída com sucesso!')
            return redirect('lista_manutencoes')
        except Exception as e:
            messages.error(request, f'Não foi possível excluir a manutenção. Erro: {e}')
            return redirect('detalhes_manutencao', pk=manutencao.pk)
    return render(request, 'core/excluir_manutencao.html', {'manutencao': manutencao})
def relatorio_faturamento(request):
   
    ano_selecionado = request.GET.get('ano')
    mes_selecionado = request.GET.get('mes')

    faturamento_total = 0
    faturamento_por_mes = {} 

   
    locacoes_finalizadas = Locacao.objects.filter(
        data_fim_real__isnull=False, 
        valor_total__isnull=False 
    ).order_by('data_fim_real') 

    
    if ano_selecionado:
        locacoes_finalizadas = locacoes_finalizadas.filter(data_fim_real__year=ano_selecionado)
    if mes_selecionado:
        locacoes_finalizadas = locacoes_finalizadas.filter(data_fim_real__month=mes_selecionado)

    
    if locacoes_finalizadas.exists():
        faturamento_total = locacoes_finalizadas.aggregate(total=Sum('valor_total'))['total'] or 0

       
        faturamento_agregado = locacoes_finalizadas \
            .annotate(
                ano=ExtractYear('data_fim_real'),
                mes=ExtractMonth('data_fim_real')
            ) \
            .values('ano', 'mes') \
            .annotate(soma_mensal=Sum('valor_total')) \
            .order_by('ano', 'mes')

        for item in faturamento_agregado:
            chave = f"{item['ano']}-{str(item['mes']).zfill(2)}" 
            faturamento_por_mes[chave] = item['soma_mensal']

    
    context = {
        'faturamento_total': faturamento_total,
        'faturamento_por_mes': faturamento_por_mes,
        'ano_selecionado': ano_selecionado,
        'mes_selecionado': mes_selecionado,
    }
    return render(request, 'core/relatorio_faturamento.html', context)