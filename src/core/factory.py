from src.core.use_cases.demanda_repository import DemandaRepository
from src.core.use_cases.demanda_dao import DemandaDAO

class DemandaFactory:
    def obter_demanda_dao(self):
        return DemandaDAO()

    def obter_demanda_repository(self):
        return DemandaRepository(self.obter_demanda_dao())