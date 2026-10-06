from core.use_cases.repositories.demanda_repository import DemandaRepository
from core.use_cases.repositories.servico_repository import ServicoRepository
from core.use_cases.repositories.trabalho_repository import TrabalhoRepository
from core.use_cases.repositories.proposta_repository import PropostaRepository
from core.use_cases.dao.demanda_dao import DemandaDAO
from core.use_cases.dao.servico_dao import ServicoDAO
from core.use_cases.dao.trabalho_dao import TrabalhoDAO
from core.use_cases.dao.proposta_dao import PropostaDAO

class Factory:
    def obter_demanda_dao(self):
        return DemandaDAO()

    def obter_servico_dao(self):
        return ServicoDAO()

    def obter_demanda_repository(self):
        return DemandaRepository(self.obter_demanda_dao())

    def obter_servico_repository(self):
        return ServicoRepository(self.obter_servico_dao())

    def obter_trabalho_dao(self):
        return TrabalhoDAO()
    
    def obter_trabalho_repository(self):
        return TrabalhoRepository(self.obter_trabalho_dao())
    
    def obter_proposta_dao(self):
        return PropostaDAO()
    
    def obter_proposta_repository(self):
        return PropostaRepository(self.obter_proposta_dao())