from src.core.use_cases.proposta_dao import PropostaDAO
from src.core.use_cases.proposta_repository import PropostaRepository


class PropostaFactory:
    def obter_proposta_dao(self) -> PropostaDAO:
        return PropostaDAO()

    def obter_proposta_repository(self) -> PropostaRepository:
        return PropostaRepository(self.obter_proposta_dao())
