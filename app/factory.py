from app.dao import (
    ConexaoBD_ORM,
    DemandaDAO_ORM,
    PropostaDAO_ORM,
    ServicoDAO_ORM,
    TrabalhoDAO_ORM,
)
from core.factory import Factory


class ServicosFactory(Factory):
    """Factory do core, trocando os DAOs em memória pelos DAOs com ORM."""

    def obter_conexao_bd(self):
        return ConexaoBD_ORM()

    def obter_trabalho_dao(self):
        return TrabalhoDAO_ORM(self.obter_conexao_bd())

    def obter_servico_dao(self):
        return ServicoDAO_ORM(self.obter_conexao_bd())

    def obter_demanda_dao(self):
        return DemandaDAO_ORM(self.obter_conexao_bd())

    def obter_proposta_dao(self):
        return PropostaDAO_ORM(self.obter_conexao_bd())
