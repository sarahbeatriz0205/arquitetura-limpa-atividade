from core.entities.proposta import StatusProposta, TipoProposta
from core.entities.trabalho import StatusTrabalho

ROTULOS = {
    StatusTrabalho.DISPONIVEL: "Disponível",
    StatusTrabalho.INDISPONIVEL: "Indisponível",
    TipoProposta.PARA_DEMANDA: "Para demanda",
    TipoProposta.PARA_SERVICO: "Para serviço",
    StatusProposta.PENDENTE: "Pendente",
    StatusProposta.ACEITA: "Aceita",
    StatusProposta.RECUSADA: "Recusada",
    TipoTrabalho.SERVICO: "Serviço",
    TipoTrabalho.DEMANDA: "Demanda"
}


def opcoes(enum_classe) -> list[tuple[int, str]]:
    return [(item.value, ROTULOS[item]) for item in enum_classe]
