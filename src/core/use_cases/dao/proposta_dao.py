from src.core.entities.proposta import Proposta
from src.core.ports.idao.iproposta import IPropostaDAO


# DAO fake: as propostas ficam numa lista em memória
class PropostaDAO(IPropostaDAO):
    def __init__(self) -> None:
        self.propostas: list[Proposta] = []

    def obter_por_id(self, id: int) -> Proposta | None:
        for proposta in self.propostas:
            if proposta.id == id:
                return proposta
        return None

    def incluir(self, proposta: Proposta) -> Proposta:
        if self.obter_por_id(proposta.id) is not None:
            raise ValueError("Já existe uma proposta com esse id.")
        self.propostas.append(proposta)
        return proposta

    def alterar(self, proposta: Proposta) -> Proposta:
        busca = self.obter_por_id(proposta.id)
        if busca is None:
            raise ValueError("Proposta não encontrada.")
        self.propostas[self.propostas.index(busca)] = proposta
        return proposta

    def excluir(self, proposta: Proposta) -> None:
        busca = self.obter_por_id(proposta.id)
        if busca is None:
            raise ValueError("Proposta não encontrada.")
        self.propostas.remove(busca)

    def listar(self) -> list[Proposta]:
        return list(self.propostas)
