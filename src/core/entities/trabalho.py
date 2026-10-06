from dataclasses import dataclass
from enum import Enum


class StatusTrabalho(Enum):
    DISPONIVEL = 1
    INDISPONIVEL = 2


@dataclass
class Trabalho:
    id: int
    titulo: str
    descricao: str
    orcamento: str
    status: StatusTrabalho = StatusTrabalho.DISPONIVEL
