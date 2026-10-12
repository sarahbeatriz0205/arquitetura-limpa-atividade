from django.core.management.base import BaseCommand

from app.banco import criar_tabelas
from app.dao import ConexaoBD_ORM


class Command(BaseCommand):
    help = "Cria as tabelas do banco de dados (db_nexo.sqlite3)."

    def handle(self, *args, **options):
        criar_tabelas(ConexaoBD_ORM())
        self.stdout.write(self.style.SUCCESS("Banco de dados criado com sucesso."))
