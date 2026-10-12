from dataclasses import dataclass
from core.entities.trabalho import Trabalho


@dataclass
class Demanda:
    id: int  # id vem do trabalho
    exigencias: str
    prazo: str
    trabalho: Trabalho
