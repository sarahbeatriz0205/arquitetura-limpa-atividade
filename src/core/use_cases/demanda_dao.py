from src.core.entities.demanda import Demanda
from src.core.ports.idao.idemanda import IDemandaDAO

# no meu caso, todas as demandas vão ser guardadas numa lista normal (lista de objetos do tipo Demanda)
# esse modelo serve também pra as demais classes que vão ser implementadas, basta adaptar à sua implementação
demandas = [] 

# DAO fake
class DemandaDAO(IDemandaDAO):
    def obter_por_id(self, id):
            for demanda in demandas:
                if (demanda.id == id):
                    return demanda
                
    def incluir(self, demanda: Demanda) -> Demanda:
        demandas.append(demanda)

    def alterar(self, demanda: Demanda) -> Demanda:
            busca = self.obter_por_id(demanda.id)
            if busca is None:
                return "Erro! Essa demanda não existe"
            else:
                demandas.remove(busca)
                demandas.append(demanda)
                return demanda
            
    def excluir(self, demanda):
        busca = self.obter_por_id(demanda.id)
        if busca is None:
            return "Erro! Essa demanda não existe"
        else:
            demandas.remove(busca)

    def listar(self):
        return demandas