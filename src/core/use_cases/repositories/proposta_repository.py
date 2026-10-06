from src.core.entities.proposta import Proposta, StatusProposta, TipoProposta
from src.core.ports.idao.iproposta import IPropostaDAO


def _vazio(valor) -> bool:
    return not isinstance(valor, str) or valor.strip() == ""


class PropostaRepository:
    def __init__(self, dao: IPropostaDAO) -> None:
        self.dao = dao

    def validar(self, proposta: Proposta) -> None:
        if _vazio(proposta.orcamento):
            raise ValueError("O orçamento é obrigatório.")
        if _vazio(proposta.apresentacao):
            raise ValueError("A apresentação é obrigatória.")
        if _vazio(proposta.prazo):
            raise ValueError("O prazo é obrigatório.")
        if _vazio(proposta.exigencia):
            raise ValueError("A exigência é obrigatória.")
        if not isinstance(proposta.tipo, TipoProposta):
            raise ValueError("Tipo inválido.")
        if not isinstance(proposta.status, StatusProposta):
            raise ValueError("Status inválido.")

    def incluir(self, proposta: Proposta) -> Proposta:
        self.validar(proposta)
        return self.dao.incluir(proposta)

    def alterar(self, proposta: Proposta) -> Proposta:
        self.validar(proposta)
        return self.dao.alterar(proposta)

    def excluir(self, proposta: Proposta) -> None:
        self.dao.excluir(proposta)

    def obter_por_id(self, id: int) -> Proposta | None:
        return self.dao.obter_por_id(id)

    def listar(self) -> list[Proposta]:
        return self.dao.listar()
