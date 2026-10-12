from core.entities.demanda import Demanda
from core.ports.idao.idemanda import IDemandaDAO

class DemandaRepository:
    def __init__(self, dao: IDemandaDAO) -> None:
        self.dao = dao

    def obter_por_id(self, id: int) -> Demanda | None:
        return self.dao.obter_por_id(id)

    def validar(self, demanda: Demanda):
        if not demanda.exigencias or not demanda.exigencias.strip():
            raise ValueError("A exigência é obrigatória.")
        if not demanda.prazo or not demanda.prazo.strip():
            raise ValueError("O prazo é obrigatório.")

    def incluir(self, demanda: Demanda) -> Demanda:
        self.validar(demanda)
        obj = self.dao.incluir(demanda)
        return obj

    def alterar(self, demanda: Demanda) -> Demanda:
        self.validar(demanda)
        obj = self.dao.alterar(demanda)
        return obj

    def excluir(self, demanda: Demanda) -> None:
        self.dao.excluir(demanda)

    def listar(self) -> list[Demanda]:
        return self.dao.listar()