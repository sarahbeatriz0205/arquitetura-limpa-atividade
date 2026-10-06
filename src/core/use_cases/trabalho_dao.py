from src.core.entities.trabalho import Trabalho
from src.core.ports.idao.itrabalho import ITrabalhoDAO


# DAO fake: os trabalhos ficam numa lista em memória
class TrabalhoDAO(ITrabalhoDAO):
    def __init__(self) -> None:
        self.trabalhos: list[Trabalho] = []

    def obter_por_id(self, id: int) -> Trabalho | None:
        for trabalho in self.trabalhos:
            if trabalho.id == id:
                return trabalho
        return None

    def incluir(self, trabalho: Trabalho) -> Trabalho:
        if self.obter_por_id(trabalho.id) is not None:
            raise ValueError("Já existe um trabalho com esse id.")
        self.trabalhos.append(trabalho)
        return trabalho

    def alterar(self, trabalho: Trabalho) -> Trabalho:
        busca = self.obter_por_id(trabalho.id)
        if busca is None:
            raise ValueError("Trabalho não encontrado.")
        self.trabalhos[self.trabalhos.index(busca)] = trabalho
        return trabalho

    def excluir(self, trabalho: Trabalho) -> None:
        busca = self.obter_por_id(trabalho.id)
        if busca is None:
            raise ValueError("Trabalho não encontrado.")
        self.trabalhos.remove(busca)

    def listar(self) -> list[Trabalho]:
        return list(self.trabalhos)
