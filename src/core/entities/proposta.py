from dataclasses import dataclass
from enum import Enum


class TipoProposta(Enum):
    PARA_DEMANDA = 1
    PARA_SERVICO = 2


class StatusProposta(Enum):
    PENDENTE = 1
    ACEITA = 2
    RECUSADA = 3


@dataclass
class Proposta:
    id: int
    orcamento: str
    apresentacao: str
    prazo: str
    exigencia: str
    tipo: TipoProposta
    status: StatusProposta = StatusProposta.PENDENTE
