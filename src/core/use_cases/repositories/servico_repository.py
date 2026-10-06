from core.entities.servico import Servico
from src.core.ports.idao.iservico import IServicoDAO


class ServicoRepository():

    def __init__(self, dao: IServicoDAO)-> None:
        self.dao = dao 
    
    def obter_por_id(self, id: int) -> Servico:
        return self.dao.obter_por_id(id)
        
    def validar(self, servico:Servico):
        if not servico.metodologia or not servico.metodologia.strip():
            raise ValueError("A metodologia é obrigatória.")
        if not servico.ferramenta or not servico.ferramenta.strip():
            raise ValueError("A ferramenta é obrigatória.")

    def incluir(self, servico: Servico) -> Servico:
        self.validar(servico)
        return self.dao.incluir(servico)
    
    def alterar(self, servico: Servico) -> Servico:
        self.validar(servico)
        return self.dao.alterar(servico)

    def excluir(self, id: int):
        self.dao.excluir(id)   
        
    def listar(self) -> list[Servico]:
        return self.dao.listar()