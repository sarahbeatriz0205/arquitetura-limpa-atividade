from core.entities.servico import Servico
from core.ports.idao.iservico import IServicoDAO



class ServicoDAO(IServicoDAO):
    def __init__(self) -> None:
        self.servicos: list[Servico] = []

    def incluir(self, servico: Servico) -> Servico:
        self.servicos.append(servico)
        return servico

    def alterar(self, servico: Servico) -> Servico:
        busca = self.obter_por_id(servico.id)
        if busca is None:
            raise ValueError("Serviço não encontrado.")
        self.servicos[self.servicos.index(busca)] = servico
        return servico

    def excluir(self, id: int):
        self.servicos = [s for s in self.servicos if s.id != id]

    def obter_por_id(self, id: int) -> Servico | None:
        for servico in self.servicos:
            if servico.id == id:
                return servico
        return None

    def listar(self) -> list[Servico]:
        return list(self.servicos)
