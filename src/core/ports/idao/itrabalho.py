from abc import ABC, abstractmethod

from src.core.entities.trabalho import Trabalho


class ITrabalhoDAO(ABC):
    @abstractmethod
    def incluir(self, trabalho: Trabalho) -> Trabalho:
        pass

    @abstractmethod
    def alterar(self, trabalho: Trabalho) -> Trabalho:
        pass

    @abstractmethod
    def excluir(self, trabalho: Trabalho) -> None:
        pass

    @abstractmethod
    def obter_por_id(self, id: int) -> Trabalho | None:
        pass

    @abstractmethod
    def listar(self) -> list[Trabalho]:
        pass
