from django.contrib import admin
from .models import (
    TipoVeiculo, Veiculo, Cliente, Funcionario, Agencia, Acessorio,
    Locacao, Pagamento, VeiculoAcessorio, HistoricoQuilometragem, Manutencao
)

admin.site.register(TipoVeiculo)
admin.site.register(Veiculo)
admin.site.register(Cliente)
admin.site.register(Funcionario)
admin.site.register(Agencia)
admin.site.register(Acessorio)
admin.site.register(Locacao)
admin.site.register(Pagamento)
admin.site.register(VeiculoAcessorio)
admin.site.register(HistoricoQuilometragem)
admin.site.register(Manutencao)
