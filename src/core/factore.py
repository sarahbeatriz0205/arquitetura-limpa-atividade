from src.core.use_cases.repositories import ServicoRepository
from src.core.idao.ports.idao import IServicoDAO

class ServicoFactory:
    def obter_servico_repository(self, dao: IServicoDAO) -> ServicoRepository:
        return ServicoRepository(dao)
    
    def obter_servico_dao(self) -> IServicoDAO:
        return ServicoDAO()