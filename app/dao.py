from dataclasses import asdict
from typing import Any

from django.conf import settings
from django.db import connections
from django.forms.models import model_to_dict

from app.models import DemandaModel, PropostaModel, ServicoModel, TrabalhoModel
from core.entities.demanda import Demanda
from core.entities.proposta import Proposta, StatusProposta, TipoProposta
from core.entities.servico import Servico
from core.entities.trabalho import StatusTrabalho, Trabalho
from core.ports.idao.iconexao_bd import IConexaoBD
from core.ports.idao.idemanda import IDemandaDAO
from core.ports.idao.iproposta import IPropostaDAO
from core.ports.idao.iservico import IServicoDAO
from core.ports.idao.itrabalho import ITrabalhoDAO


class ConexaoBD_ORM(IConexaoBD):
    DB_ALIAS = "db_nexo"
    DB_NAME = settings.BASE_DIR / "db_nexo.sqlite3"

    def obter_conexao(self):
        """Estabelece a conexao com o SQLite usando o ORM do Django"""

        if self.DB_ALIAS not in connections.databases:
            connections.databases[self.DB_ALIAS] = {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": self.DB_NAME,
                "ATOMIC_REQUESTS": False,
                "TIME_ZONE": "America/Fortaleza",
                "CONN_HEALTH_CHECKS": True,
                "CONN_MAX_AGE": 60,
                "AUTOCOMMIT": True,
                "OPTIONS": {},
            }

        return connections[self.DB_ALIAS]

    def executar_comando(self, sql_comando, commit=True) -> Any:
        """Executa um comando SQL no BD (geralmente um INSERT, UPDATE ou DELETE)"""
        conexao = self.obter_conexao()
        return conexao.cursor().execute(sql_comando)

    def executar_select(self, sql_select) -> list[Any]:
        """Executa um comando SELECT no BD e retorna os registros"""
        conexao = self.obter_conexao()
        return conexao.cursor().execute(sql_select).fetchall()


class TrabalhoDAO_ORM(ITrabalhoDAO):
    def __init__(self, conexao: IConexaoBD):
        self._conexao = conexao
        self._conexao.obter_conexao()

    @staticmethod
    def helper_converter_model_para_dominio(model_instance) -> Trabalho:
        trabalho_dict = model_to_dict(model_instance)
        trabalho_dict["status"] = StatusTrabalho(model_instance.status)
        return Trabalho(**trabalho_dict)

    def incluir(self, obj: Trabalho) -> Trabalho:
        obj_asdict = asdict(obj)
        obj_asdict["status"] = obj.status.value
        model_instance = TrabalhoModel(**obj_asdict)
        model_instance.save(using=self._conexao.DB_ALIAS)
        return self.helper_converter_model_para_dominio(model_instance)

    def alterar(self, obj: Trabalho) -> Trabalho:
        if not self._existe(obj.id):
            raise ValueError("Trabalho não encontrado.")
        return self.incluir(obj)

    def excluir(self, obj: Trabalho) -> None:
        apagados, _ = (
            TrabalhoModel.objects.using(self._conexao.DB_ALIAS)
            .filter(pk=obj.id)
            .delete()
        )
        if apagados == 0:
            raise ValueError("Trabalho não encontrado.")

    def obter_por_id(self, id: int) -> Trabalho | None:
        registro = (
            TrabalhoModel.objects.using(self._conexao.DB_ALIAS).filter(pk=id).first()
        )
        if registro is None:
            return None
        return self.helper_converter_model_para_dominio(registro)

    def listar(self) -> list[Trabalho]:
        registros = (
            TrabalhoModel.objects.using(self._conexao.DB_ALIAS).all().order_by("titulo")
        )
        return [self.helper_converter_model_para_dominio(r) for r in registros]

    def _existe(self, id) -> bool:
        return TrabalhoModel.objects.using(self._conexao.DB_ALIAS).filter(pk=id).exists()


class ServicoDAO_ORM(IServicoDAO):
    def __init__(self, conexao: IConexaoBD):
        self._conexao = conexao
        self._conexao.obter_conexao()

    @staticmethod
    def helper_converter_model_para_dominio(model_instance) -> Servico:
        servico_dict = model_to_dict(model_instance)
        servico_dict.pop("trabalho")
        servico = Servico(
            id=model_instance.pk,
            trabalho=TrabalhoDAO_ORM.helper_converter_model_para_dominio(
                model_instance.trabalho
            ),
            **servico_dict,
        )
        return servico

    def incluir(self, obj: Servico) -> Servico:
        obj_asdict = asdict(obj)
        obj_asdict.pop("id")
        obj_asdict.pop("trabalho")
        model_instance = ServicoModel(**obj_asdict)
        model_instance.trabalho_id = obj.trabalho.id
        model_instance.save(using=self._conexao.DB_ALIAS)
        return self.helper_converter_model_para_dominio(model_instance)

    def alterar(self, obj: Servico) -> Servico:
        if self.obter_por_id(obj.id) is None:
            raise ValueError("Serviço não encontrado.")
        return self.incluir(obj)

    def excluir(self, id: int):
        apagados, _ = (
            ServicoModel.objects.using(self._conexao.DB_ALIAS).filter(pk=id).delete()
        )
        if apagados == 0:
            raise ValueError("Serviço não encontrado.")
        if not DemandaModel.objects.using(self._conexao.DB_ALIAS).filter(pk=id).exists():
            TrabalhoModel.objects.using(self._conexao.DB_ALIAS).filter(pk=id).delete()

    def obter_por_id(self, id: int) -> Servico | None:
        registro = (
            ServicoModel.objects.using(self._conexao.DB_ALIAS)
            .select_related("trabalho")
            .filter(pk=id)
            .first()
        )
        if registro is None:
            return None
        return self.helper_converter_model_para_dominio(registro)

    def listar(self) -> list[Servico]:
        registros = (
            ServicoModel.objects.using(self._conexao.DB_ALIAS)
            .select_related("trabalho")
            .all()
            .order_by("trabalho__titulo")
        )
        return [self.helper_converter_model_para_dominio(r) for r in registros]


class DemandaDAO_ORM(IDemandaDAO):
    def __init__(self, conexao: IConexaoBD):
        self._conexao = conexao
        self._conexao.obter_conexao()

    @staticmethod
    def helper_converter_model_para_dominio(model_instance) -> Demanda:
        demanda_dict = model_to_dict(model_instance)
        demanda_dict.pop("trabalho")
        demanda = Demanda(
            id=model_instance.pk,
            trabalho=TrabalhoDAO_ORM.helper_converter_model_para_dominio(
                model_instance.trabalho
            ),
            **demanda_dict,
        )
        return demanda

    def incluir(self, obj: Demanda) -> Demanda:
        obj_asdict = asdict(obj)
        obj_asdict.pop("id")
        obj_asdict.pop("trabalho")
        model_instance = DemandaModel(**obj_asdict)
        model_instance.trabalho_id = obj.trabalho.id
        model_instance.save(using=self._conexao.DB_ALIAS)
        return self.helper_converter_model_para_dominio(model_instance)

    def alterar(self, obj: Demanda) -> Demanda:
        if self.obter_por_id(obj.id) is None:
            raise ValueError("Demanda não encontrada.")
        return self.incluir(obj)

    def excluir(self, obj: Demanda) -> None:
        apagados, _ = (
            DemandaModel.objects.using(self._conexao.DB_ALIAS).filter(pk=obj.id).delete()
        )
        if apagados == 0:
            raise ValueError("Demanda não encontrada.")
        if not ServicoModel.objects.using(self._conexao.DB_ALIAS).filter(pk=obj.id).exists():
            TrabalhoModel.objects.using(self._conexao.DB_ALIAS).filter(pk=obj.id).delete()

    def obter_por_id(self, id: int) -> Demanda | None:
        registro = (
            DemandaModel.objects.using(self._conexao.DB_ALIAS)
            .select_related("trabalho")
            .filter(pk=id)
            .first()
        )
        if registro is None:
            return None
        return self.helper_converter_model_para_dominio(registro)

    def listar(self) -> list[Demanda]:
        registros = (
            DemandaModel.objects.using(self._conexao.DB_ALIAS)
            .select_related("trabalho")
            .all()
            .order_by("trabalho__titulo")
        )
        return [self.helper_converter_model_para_dominio(r) for r in registros]


class PropostaDAO_ORM(IPropostaDAO):
    def __init__(self, conexao: IConexaoBD):
        self._conexao = conexao
        self._conexao.obter_conexao()

    @staticmethod
    def helper_converter_model_para_dominio(model_instance) -> Proposta:
        proposta_dict = model_to_dict(model_instance)
        proposta_dict["tipo"] = TipoProposta(model_instance.tipo)
        proposta_dict["status"] = StatusProposta(model_instance.status)
        return Proposta(**proposta_dict)

    def incluir(self, obj: Proposta) -> Proposta:
        obj_asdict = asdict(obj)
        obj_asdict["tipo"] = obj.tipo.value
        obj_asdict["status"] = obj.status.value
        model_instance = PropostaModel(**obj_asdict)
        model_instance.save(using=self._conexao.DB_ALIAS)
        return self.helper_converter_model_para_dominio(model_instance)

    def alterar(self, obj: Proposta) -> Proposta:
        if self.obter_por_id(obj.id) is None:
            raise ValueError("Proposta não encontrada.")
        return self.incluir(obj)

    def excluir(self, obj: Proposta) -> None:
        apagados, _ = (
            PropostaModel.objects.using(self._conexao.DB_ALIAS).filter(pk=obj.id).delete()
        )
        if apagados == 0:
            raise ValueError("Proposta não encontrada.")

    def obter_por_id(self, id: int) -> Proposta | None:
        registro = (
            PropostaModel.objects.using(self._conexao.DB_ALIAS).filter(pk=id).first()
        )
        if registro is None:
            return None
        return self.helper_converter_model_para_dominio(registro)

    def listar(self) -> list[Proposta]:
        registros = PropostaModel.objects.using(self._conexao.DB_ALIAS).all().order_by("id")
        return [self.helper_converter_model_para_dominio(r) for r in registros]
