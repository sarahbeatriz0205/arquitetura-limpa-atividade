from src.core.entities.proposta import Proposta, StatusProposta, TipoProposta
from src.core.entities.trabalho import StatusTrabalho, Trabalho
from src.core.factory_proposta import PropostaFactory
from src.core.factory_trabalho import TrabalhoFactory


def espera_erro(funcao, *args):
    try:
        funcao(*args)
    except ValueError as e:
        return f"ValueError: {e}"
    raise AssertionError("Era esperado um ValueError")


print("=== TRABALHO ===")
repo = TrabalhoFactory().obter_trabalho_repository()
t1 = Trabalho(1, "Site institucional", "Landing page responsiva", "R$ 1500")
t2 = Trabalho(2, "API REST", "API em Python", "R$ 3000")
repo.incluir(t1)
repo.incluir(t2)
assert len(repo.listar()) == 2
assert repo.obter_por_id(1) == t1
assert repo.obter_por_id(99) is None
t1_novo = Trabalho(1, "Site institucional v2", "Com blog", "R$ 2000", StatusTrabalho.INDISPONIVEL)
repo.alterar(t1_novo)
assert repo.obter_por_id(1).status == StatusTrabalho.INDISPONIVEL
print(espera_erro(repo.alterar, Trabalho(99, "x", "y", "z")))
print(espera_erro(repo.excluir, Trabalho(99, "x", "y", "z")))
print(espera_erro(repo.incluir, Trabalho(3, "  ", "y", "z")))
print(espera_erro(repo.incluir, Trabalho(1, "dup", "y", "z")))
repo.excluir(t2)
assert [t.id for t in repo.listar()] == [1]
print("Trabalho OK\n")

print("=== PROPOSTA ===")
repo = PropostaFactory().obter_proposta_repository()
p1 = Proposta(1, "R$ 1200", "Sou dev full stack", "2 semanas", "Acesso ao servidor", TipoProposta.PARA_DEMANDA)
p2 = Proposta(2, "R$ 800", "Experiência com Nginx", "1 semana", "Briefing completo", TipoProposta.PARA_SERVICO)
repo.incluir(p1)
repo.incluir(p2)
assert len(repo.listar()) == 2
assert repo.obter_por_id(1).status == StatusProposta.PENDENTE
assert repo.obter_por_id(99) is None
p1_aceita = Proposta(1, "R$ 1200", "Sou dev full stack", "2 semanas", "Acesso ao servidor",
                     TipoProposta.PARA_DEMANDA, StatusProposta.ACEITA)
repo.alterar(p1_aceita)
assert repo.obter_por_id(1).status == StatusProposta.ACEITA
print(espera_erro(repo.alterar, Proposta(99, "a", "b", "c", "d", TipoProposta.PARA_SERVICO)))
print(espera_erro(repo.excluir, Proposta(99, "a", "b", "c", "d", TipoProposta.PARA_SERVICO)))
print(espera_erro(repo.incluir, Proposta(3, "", "b", "c", "d", TipoProposta.PARA_SERVICO)))
print(espera_erro(repo.incluir, Proposta(4, "a", "b", "c", "d", "demanda")))
repo.excluir(p2)
assert [p.id for p in repo.listar()] == [1]
print("Proposta OK")
