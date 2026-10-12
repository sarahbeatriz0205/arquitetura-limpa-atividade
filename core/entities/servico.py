from dataclasses import dataclass
from core.entities.trabalho import Trabalho

@dataclass
class Servico:
    id: int
    metodologia: str
    ferramenta: str
    trabalho: Trabalho