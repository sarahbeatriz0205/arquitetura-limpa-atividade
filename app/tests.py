import itertools
import unittest
from unittest import mock

from django.db import connections
from django.test import Client

from app.banco import criar_tabelas
from app.dao import ConexaoBD_ORM
from app.factory import ServicosFactory
from core.entities.proposta import Proposta, StatusProposta, TipoProposta
from core.entities.trabalho import StatusTrabalho, Trabalho

_contador = itertools.count(1)


class BancoEmMemoriaTestCase(unittest.TestCase):
    """Cada teste usa um banco SQLite em memória próprio (o db_nexo.sqlite3 não é alterado)."""

    def assertContains(self, resposta, texto):
        self.assertEqual(resposta.status_code, 200)
        self.assertIn(texto, resposta.content.decode())

    def setUp(self):
        self.alias = f"db_teste_{next(_contador)}"
        for atributo, valor in (("DB_ALIAS", self.alias), ("DB_NAME", ":memory:")):
            patcher = mock.patch.object(ConexaoBD_ORM, atributo, valor)
            patcher.start()
            self.addCleanup(patcher.stop)
        self.addCleanup(self._remover_conexao)
        criar_tabelas(ConexaoBD_ORM())
        self.fabrica = ServicosFactory()
        self.client = Client()

    def _remover_conexao(self):
        connections[self.alias].close()
        del connections[self.alias]
        del connections.databases[self.alias]


class RepositoriesComOrmTest(BancoEmMemoriaTestCase):
    def test_trabalho_incluir_listar_alterar_excluir(self):
        repo = self.fabrica.obter_trabalho_repository()
        trabalho = repo.incluir(Trabalho(None, "Site", "Criar site", "1000"))
        self.assertIsNotNone(trabalho.id)
        self.assertEqual(len(repo.listar()), 1)

        trabalho.titulo = "Site novo"
        trabalho.status = StatusTrabalho.INDISPONIVEL
        repo.alterar(trabalho)
        salvo = repo.obter_por_id(trabalho.id)
        self.assertEqual(salvo.titulo, "Site novo")
        self.assertEqual(salvo.status, StatusTrabalho.INDISPONIVEL)

        repo.excluir(salvo)
        self.assertIsNone(repo.obter_por_id(trabalho.id))

    def test_trabalho_validacao_do_core(self):
        repo = self.fabrica.obter_trabalho_repository()
        with self.assertRaises(ValueError):
            repo.incluir(Trabalho(None, "  ", "desc", "10"))

    def test_alterar_inexistente_gera_erro(self):
        repo = self.fabrica.obter_trabalho_repository()
        with self.assertRaises(ValueError):
            repo.alterar(Trabalho(999, "x", "y", "1"))

    def test_proposta_validacao_e_status_padrao(self):
        repo = self.fabrica.obter_proposta_repository()
        with self.assertRaises(ValueError):
            repo.incluir(
                Proposta(None, "", "apresentação", "5 dias", "nenhuma", TipoProposta.PARA_DEMANDA)
            )
        proposta = repo.incluir(
            Proposta(None, "500", "apresentação", "5 dias", "nenhuma", TipoProposta.PARA_SERVICO)
        )
        self.assertEqual(repo.obter_por_id(proposta.id).status, StatusProposta.PENDENTE)
        self.assertEqual(repo.obter_por_id(proposta.id).tipo, TipoProposta.PARA_SERVICO)


class CrudWebTest(BancoEmMemoriaTestCase):
    def test_home_e_listagens(self):
        for rota in ("/", "/trabalhos/", "/servicos/", "/demandas/", "/propostas/"):
            self.assertEqual(self.client.get(rota).status_code, 200, rota)

    def test_trabalho_crud(self):
        dados = {"acao": "Inclusão", "titulo": "Logo", "descricao": "Criar logo",
                 "orcamento": "300", "status": 1}
        resposta = self.client.post("/trabalhos/salvar/", dados)
        self.assertEqual(resposta.status_code, 302)

        trabalho = self.fabrica.obter_trabalho_repository().listar()[0]
        self.assertContains(self.client.get("/trabalhos/"), "Logo")
        self.assertContains(self.client.get("/trabalhos/incluir/"), "Título")

        dados.update(acao="Alteração", id=trabalho.id, titulo="Logo v2")
        self.client.post("/trabalhos/salvar/", dados)
        self.assertEqual(
            self.fabrica.obter_trabalho_repository().obter_por_id(trabalho.id).titulo, "Logo v2"
        )
        self.assertContains(self.client.get(f"/trabalhos/alterar/{trabalho.id}/"), "Logo v2")
        self.assertContains(self.client.get(f"/trabalhos/excluir/{trabalho.id}/"), "Deseja realmente")

        self.client.post("/trabalhos/salvar/", {"acao": "Exclusão", "id": trabalho.id})
        self.assertEqual(self.fabrica.obter_trabalho_repository().listar(), [])

    def test_trabalho_invalido_exibe_erro(self):
        dados = {"acao": "Inclusão", "titulo": "  ", "descricao": "x", "orcamento": "1", "status": 1}
        resposta = self.client.post("/trabalhos/salvar/", dados)
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, "O título é obrigatório.")

    def test_servico_crud(self):
        dados = {"acao": "Inclusão", "titulo": "Consultoria", "descricao": "Consultoria em TI",
                 "orcamento": "2000", "status": 1, "metodologia": "Scrum", "ferramenta": "Jira"}
        self.assertEqual(self.client.post("/servicos/salvar/", dados).status_code, 302)
        repo = self.fabrica.obter_servico_repository()
        servico = repo.listar()[0]
        self.assertEqual(servico.trabalho.titulo, "Consultoria")
        self.assertEqual(servico.id, servico.trabalho.id)

        dados.update(acao="Alteração", id=servico.id, metodologia="Kanban", titulo="Consultoria 2")
        self.client.post("/servicos/salvar/", dados)
        alterado = repo.obter_por_id(servico.id)
        self.assertEqual(alterado.metodologia, "Kanban")
        self.assertEqual(alterado.trabalho.titulo, "Consultoria 2")
        self.assertContains(self.client.get(f"/servicos/alterar/{servico.id}/"), "Kanban")

        self.client.post("/servicos/salvar/", {"acao": "Exclusão", "id": servico.id})
        self.assertEqual(repo.listar(), [])
        self.assertEqual(self.fabrica.obter_trabalho_repository().listar(), [])

    def test_servico_invalido_nao_grava_trabalho(self):
        dados = {"acao": "Inclusão", "titulo": "Sem ferramenta", "descricao": "x",
                 "orcamento": "1", "status": 1, "metodologia": "Scrum", "ferramenta": ""}
        resposta = self.client.post("/servicos/salvar/", dados)
        self.assertContains(resposta, "A ferramenta é obrigatória.")
        self.assertEqual(self.fabrica.obter_trabalho_repository().listar(), [])

    def test_demanda_crud(self):
        dados = {"acao": "Inclusão", "titulo": "App mobile", "descricao": "Preciso de um app",
                 "orcamento": "5000", "status": 1, "exigencias": "Android e iOS", "prazo": "60 dias"}
        self.assertEqual(self.client.post("/demandas/salvar/", dados).status_code, 302)
        repo = self.fabrica.obter_demanda_repository()
        demanda = repo.listar()[0]
        self.assertEqual(demanda.prazo, "60 dias")

        dados.update(acao="Alteração", id=demanda.id, prazo="90 dias")
        self.client.post("/demandas/salvar/", dados)
        self.assertEqual(repo.obter_por_id(demanda.id).prazo, "90 dias")

        self.client.post("/demandas/salvar/", {"acao": "Exclusão", "id": demanda.id})
        self.assertEqual(repo.listar(), [])
        self.assertEqual(self.fabrica.obter_trabalho_repository().listar(), [])

    def test_proposta_crud(self):
        dados = {"acao": "Inclusão", "orcamento": "4500", "apresentacao": "Tenho experiência",
                 "prazo": "45 dias", "exigencia": "Pagamento em duas parcelas", "tipo": 1, "status": 1}
        self.assertEqual(self.client.post("/propostas/salvar/", dados).status_code, 302)
        repo = self.fabrica.obter_proposta_repository()
        proposta = repo.listar()[0]

        dados.update(acao="Alteração", id=proposta.id, status=2)
        self.client.post("/propostas/salvar/", dados)
        self.assertEqual(repo.obter_por_id(proposta.id).status, StatusProposta.ACEITA)
        self.assertContains(self.client.get("/propostas/"), "Aceita")

        self.client.post("/propostas/salvar/", {"acao": "Exclusão", "id": proposta.id})
        self.assertEqual(repo.listar(), [])

    def test_registro_inexistente_exibe_erro(self):
        resposta = self.client.get("/servicos/alterar/999/")
        self.assertContains(resposta, "Registro não encontrado.")
