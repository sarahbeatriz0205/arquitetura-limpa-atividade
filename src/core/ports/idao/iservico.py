from abc import ABC
from src.core.entities.servico import Servico

class IServicoDAO(ABC):
    def incluir(self, obj: Servico) -> Servico:
        pass
    
    def alterar(self, obj: Servico) -> Servico:
        pass
    
    def excluir(self, id: int):
        pass

    def obter_por_id(self, id: int) -> Servico:
        pass
    
    def listar(self) -> list[Servico]:
        pass