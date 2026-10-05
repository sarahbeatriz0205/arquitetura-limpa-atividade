from dataclasses import dataclass

@dataclass
class Demanda:
    id: int # id vem do trabalho
    exigencias: str
    prazo: str

    def __init__(self, id: int, exigencias: str, prazo: str):
        self.id = id
        self.exigencias = exigencias
        self.prazo = prazo