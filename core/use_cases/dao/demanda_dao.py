from core.entities.demanda import Demanda
from core.ports.idao.idemanda import IDemandaDAO


# DAO fake: as demandas ficam numa lista em memória
class DemandaDAO(IDemandaDAO):
    def __init__(self) -> None:
        self.demandas: list[Demanda] = []

    def obter_por_id(self, id: int) -> Demanda | None:
        for demanda in self.demandas:
            if demanda.id == id:
                return demanda
        return None

    def incluir(self, demanda: Demanda) -> Demanda:
        self.demandas.append(demanda)
        return demanda

    def alterar(self, demanda: Demanda) -> Demanda:
        busca = self.obter_por_id(demanda.id)
        if busca is None:
            raise ValueError("Demanda não encontrada.")
        self.demandas[self.demandas.index(busca)] = demanda
        return demanda

    def excluir(self, demanda: Demanda) -> None:
        busca = self.obter_por_id(demanda.id)
        if busca is None:
            raise ValueError("Demanda não encontrada.")
        self.demandas.remove(busca)

    def listar(self) -> list[Demanda]:
        return list(self.demandas)
