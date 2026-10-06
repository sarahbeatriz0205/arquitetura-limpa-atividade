from dataclasses import dataclass
from src.core.entities.trabalho import Trabalho

@dataclass
class Demanda:
    id: int # id vem do trabalho
    exigencias: str
    prazo: str
    trabalho: Trabalho

    def __init__(self, id: int, exigencias: str, prazo: str, trabalho: Trabalho):
        self.id = id
        self.exigencias = exigencias
        self.prazo = prazo
        self.trabalho: Trabalho