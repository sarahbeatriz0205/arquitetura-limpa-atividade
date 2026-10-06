from abc import ABC, abstractmethod

from src.core.entities.proposta import Proposta


class IPropostaDAO(ABC):
    @abstractmethod
    def incluir(self, proposta: Proposta) -> Proposta:
        pass

    @abstractmethod
    def alterar(self, proposta: Proposta) -> Proposta:
        pass

    @abstractmethod
    def excluir(self, proposta: Proposta) -> None:
        pass

    @abstractmethod
    def obter_por_id(self, id: int) -> Proposta | None:
        pass

    @abstractmethod
    def listar(self) -> list[Proposta]:
        pass
