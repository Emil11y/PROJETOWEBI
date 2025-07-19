from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('veiculos/', views.lista_veiculos, name='lista_veiculos'), # Lista todos os veículos
    path('veiculos/adicionar/', views.adicionar_veiculo, name='adicionar_veiculo'), # Formulário para adicionar
    path('veiculos/<int:pk>/', views.detalhes_veiculo, name='detalhes_veiculo'), # Detalhes de um veículo específico
    path('veiculos/<int:pk>/editar/', views.editar_veiculo, name='editar_veiculo'), # Formulário para editar
    path('veiculos/<int:pk>/excluir/', views.excluir_veiculo, name='excluir_veiculo'), # Confirmação de exclusão

#clientes
 path('clientes/', views.lista_clientes, name='lista_clientes'),
    path('clientes/adicionar/', views.adicionar_cliente, name='adicionar_cliente'),
    path('clientes/<int:pk>/', views.detalhes_cliente, name='detalhes_cliente'),
    path('clientes/<int:pk>/editar/', views.editar_cliente, name='editar_cliente'),
    path('clientes/<int:pk>/excluir/', views.excluir_cliente, name='excluir_cliente'),

    path('locacoes/', views.lista_locacoes, name='lista_locacoes'),
    path('locacoes/adicionar/', views.adicionar_locacao, name='adicionar_locacao'),
    path('locacoes/<int:pk>/', views.detalhes_locacao, name='detalhes_locacao'),
    path('locacoes/<int:pk>/editar/', views.editar_locacao, name='editar_locacao'),
    path('locacoes/<int:pk>/excluir/', views.excluir_locacao, name='excluir_locacao'),
    
    path('funcionarios/', views.lista_funcionarios, name='lista_funcionarios'),
    path('funcionarios/adicionar/', views.adicionar_funcionario, name='adicionar_funcionario'),
    path('funcionarios/<int:pk>/', views.detalhes_funcionario, name='detalhes_funcionario'),
    path('funcionarios/<int:pk>/editar/', views.editar_funcionario, name='editar_funcionario'),
    path('funcionarios/<int:pk>/excluir/', views.excluir_funcionario, name='excluir_funcionario'),

    path('agencias/', views.lista_agencias, name='lista_agencias'),
    path('agencias/adicionar/', views.adicionar_agencia, name='adicionar_agencia'),
    path('agencias/<int:pk>/', views.detalhes_agencia, name='detalhes_agencia'),
    path('agencias/<int:pk>/editar/', views.editar_agencia, name='editar_agencia'),
    path('agencias/<int:pk>/excluir/', views.excluir_agencia, name='excluir_agencia'),

    path('acessorios/', views.lista_acessorios, name='lista_acessorios'),
    path('acessorios/adicionar/', views.adicionar_acessorio, name='adicionar_acessorio'),
    path('acessorios/<int:pk>/', views.detalhes_acessorio, name='detalhes_acessorio'),
    path('acessorios/<int:pk>/editar/', views.editar_acessorio, name='editar_acessorio'),
    path('acessorios/<int:pk>/excluir/', views.excluir_acessorio, name='excluir_acessorio'),

    path('pagamentos/', views.lista_pagamentos, name='lista_pagamentos'),
    path('pagamentos/adicionar/', views.adicionar_pagamento, name='adicionar_pagamento'),
    path('pagamentos/<int:pk>/', views.detalhes_pagamento, name='detalhes_pagamento'),
    path('pagamentos/<int:pk>/editar/', views.editar_pagamento, name='editar_pagamento'),
    path('pagamentos/<int:pk>/excluir/', views.excluir_pagamento, name='excluir_pagamento'),

    path('historico_quilometragem/', views.lista_historico_quilometragem, name='lista_historico_quilometragem'),
    path('historico_quilometragem/adicionar/', views.adicionar_historico_quilometragem, name='adicionar_historico_quilometragem'),
    path('historico_quilometragem/<int:pk>/', views.detalhes_historico_quilometragem, name='detalhes_historico_quilometragem'),
    path('historico_quilometragem/<int:pk>/editar/', views.editar_historico_quilometragem, name='editar_historico_quilometragem'),
    path('historico_quilometragem/<int:pk>/excluir/', views.excluir_historico_quilometragem, name='excluir_historico_quilometragem'),


    path('veiculo_acessorios/', views.lista_veiculo_acessorios, name='lista_veiculo_acessorios'),
    path('veiculo_acessorios/adicionar/', views.adicionar_veiculo_acessorio, name='adicionar_veiculo_acessorio'),
    path('veiculo_acessorios/<int:pk>/', views.detalhes_veiculo_acessorio, name='detalhes_veiculo_acessorio'),
    path('veiculo_acessorios/<int:pk>/editar/', views.editar_veiculo_acessorio, name='editar_veiculo_acessorio'),
    path('veiculo_acessorios/<int:pk>/excluir/', views.excluir_veiculo_acessorio, name='excluir_veiculo_acessorio'),

    path('manutencoes/', views.lista_manutencoes, name='lista_manutencoes'),
    path('manutencoes/adicionar/', views.adicionar_manutencao, name='adicionar_manutencao'),
    path('manutencoes/<int:pk>/', views.detalhes_manutencao, name='detalhes_manutencao'),
    path('manutencoes/<int:pk>/editar/', views.editar_manutencao, name='editar_manutencao'),
    path('manutencoes/<int:pk>/excluir/', views.excluir_manutencao, name='excluir_manutencao'),
    path('relatorios/faturamento/', views.relatorio_faturamento, name='relatorio_faturamento'),
    ]