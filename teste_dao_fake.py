from src.core.factory import DemandaFactory
from src.core.entities.demanda import Demanda

demanda_repository = DemandaFactory().obter_demanda_repository()

print("--- Começando os testes diretos ---\n")

# 1. Criando e incluindo objetos Demanda
demanda1 = Demanda(id=1, exigencias="Use HTML, CSS e Javascript em todo o processo", prazo="1 semana")
demanda2 = Demanda(id=2, exigencias="Domínio de Nginx", prazo="2 semanas")

demanda_repository.incluir(demanda1)
demanda_repository.incluir(demanda2)
print("Incluído: Demanda 1 e Demanda 2 adicionadas.")

# 2. Testando o método listar
lista = demanda_repository.listar()
print(f"Listar: Encontrados {len(lista)} objetos.")
print(f"Conteúdo atual: {lista}\n")

# 3. Testando o obter_por_id
busca = demanda_repository.obter_por_id(1)
print(f"Obter por ID (1): Encontrado -> Exigências: '{busca.exigencias}'\n")

# 4. Testando o método alterar
demanda_modificada = Demanda(id=1, exigencias="HTML, CSS, JS + React", prazo="3 semanas")
retorno_alterar = demanda_repository.alterar(demanda_modificada)
print(f"Alterar (ID 1): Retorno do método -> {retorno_alterar}")

# Validando se alterou na lista interna
busca_pos_alteracao = demanda_repository.obter_por_id(1)
print(f"Validação pós-alteração (ID 1): Novo prazo é '{busca_pos_alteracao.prazo}'\n")

# 5. Testando cenários de Erro (ID inexistente)
erro_alterar = demanda_repository.alterar(Demanda(id=99, exigencias="Erro", prazo="1 dia"))
print(f"Teste de Erro ao Alterar (ID 99): {erro_alterar}")

erro_excluir = demanda_repository.excluir(Demanda(id=99, exigencias="Erro", prazo="1 dia"))
print(f"Teste de Erro ao Excluir (ID 99): {erro_excluir}\n")

# 6. Testando o método excluir
demanda_repository.excluir(demanda2)
print("Excluir: Demanda 2 removida.")

lista_final = demanda_repository.listar()
print(f"Listar final: Restaram {len(lista_final)} objetos.")
print(f"Conteúdo final: {lista_final}")