from abc import ABC


class IServicoDAO(ABC):
    @abstractmethd
    def incluir(self, obj: Servico) -> Servico:
        pass
    
    @abstractmethd
    def alterar(self, obj: Servico) -> Servico:
        pass
    
    @abstractmethd
    def excluir(self, id: int):
        pass

    @abstractmethd
    def obter_por_id(self, id: int) -> Servico:
        pass
    
    @abstractmethd
    def listar(self) -> lista[Servico]:
        pass