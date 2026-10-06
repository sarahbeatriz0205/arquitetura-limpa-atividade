from src.core.use_cases.trabalho_dao import TrabalhoDAO
from src.core.use_cases.trabalho_repository import TrabalhoRepository


class TrabalhoFactory:
    def obter_trabalho_dao(self) -> TrabalhoDAO:
        return TrabalhoDAO()

    def obter_trabalho_repository(self) -> TrabalhoRepository:
        return TrabalhoRepository(self.obter_trabalho_dao())
