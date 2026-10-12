from pathlib import Path

from core.ports.idao.iconexao_bd import IConexaoBD

CAMINHO_SCHEMA = Path(__file__).resolve().parent.parent / "banco" / "schema.sql"


def criar_tabelas(conexao: IConexaoBD) -> None:
    """Cria as tabelas do banco (se ainda não existirem) a partir de banco/schema.sql"""
    comandos = CAMINHO_SCHEMA.read_text(encoding="utf-8").split(";")
    for comando in comandos:
        if comando.strip():
            conexao.executar_comando(comando)
