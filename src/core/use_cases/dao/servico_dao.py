from core.entities.servico import Servico
from src.core.ports.idao.iservico import IServicoDAO   

servico = []

class ServicoDAO(IServicoDAO):
    def incluir(self, servico: Servico) -> Servico:
        servico.append(servico)
        return servico
    
    def alterar(self, servico: Servico) -> Servico:
        buscar = self.obter_por_id(servico.id)
        if buscar is None:
            raise ValueError("Serviço não encontrado.")
        else:
            servico.remove(buscar)
            servico.append(servico)
            return servico

    def excluir(self, id: int):
        global servico
        servico = [s for s in servico if s.id != id]

    def obter_por_id(self, id: int) -> Servico:
        for servico in servico:
            if servico.id == id:
                return servico
        raise ValueError("Serviço não encontrado.")
    
    def listar(self) -> list[Servico]:
        return servico