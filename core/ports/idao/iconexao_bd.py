from abc import ABC, abstractmethod
from typing import Any


class IConexaoBD(ABC):
    @abstractmethod
    def obter_conexao(self):
        pass

    @abstractmethod
    def executar_comando(self, sql_comando, commit=True) -> Any:
        pass

    @abstractmethod
    def executar_select(self, sql_select) -> list[Any]:
        pass
