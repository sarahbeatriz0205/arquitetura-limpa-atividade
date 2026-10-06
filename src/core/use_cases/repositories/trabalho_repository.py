from src.core.entities.trabalho import StatusTrabalho, Trabalho
from src.core.ports.idao.itrabalho import ITrabalhoDAO


def _vazio(valor) -> bool:
    return not isinstance(valor, str) or valor.strip() == ""


class TrabalhoRepository:
    def __init__(self, dao: ITrabalhoDAO) -> None:
        self.dao = dao

    def validar(self, trabalho: Trabalho) -> None:
        if _vazio(trabalho.titulo):
            raise ValueError("O título é obrigatório.")
        if _vazio(trabalho.descricao):
            raise ValueError("A descrição é obrigatória.")
        if _vazio(trabalho.orcamento):
            raise ValueError("O orçamento é obrigatório.")
        if not isinstance(trabalho.status, StatusTrabalho):
            raise ValueError("Status inválido.")

    def incluir(self, trabalho: Trabalho) -> Trabalho:
        self.validar(trabalho)
        return self.dao.incluir(trabalho)

    def alterar(self, trabalho: Trabalho) -> Trabalho:
        self.validar(trabalho)
        return self.dao.alterar(trabalho)

    def excluir(self, trabalho: Trabalho) -> None:
        self.dao.excluir(trabalho)

    def obter_por_id(self, id: int) -> Trabalho | None:
        return self.dao.obter_por_id(id)

    def listar(self) -> list[Trabalho]:
        return self.dao.listar()
