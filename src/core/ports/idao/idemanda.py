from abc import ABC
from src.core.entities.demanda import Demanda

class IDemandaDAO(ABC):
    def incluir(self, demanda: Demanda) -> Demanda:
        pass

    def alterar(self, demanda: Demanda) -> Demanda:
        pass

    def excluir(self, demanda: Demanda) -> None:
        pass

    def listar(self) -> list[Demanda]:
        pass

    def obter_por_id(self, id: int) -> Demanda:
        pass