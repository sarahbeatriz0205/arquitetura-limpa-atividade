from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from app.factory import ServicosFactory
from app.forms import DemandaForm, PropostaForm, ServicoForm, TrabalhoForm
from core.entities.demanda import Demanda
from core.entities.proposta import Proposta, StatusProposta, TipoProposta
from core.entities.servico import Servico
from core.entities.trabalho import StatusTrabalho, Trabalho


# ============================================================================
# Conversão dos dados do formulário (POST) para objetos de domínio
# ============================================================================
def _id_do_formulario(form_data):
    return int(form_data["id"]) if form_data.get("id") else None


def _trabalho_do_formulario(form_data, id=None) -> Trabalho:
    return Trabalho(
        id=id,
        titulo=form_data["titulo"],
        descricao=form_data["descricao"],
        orcamento=form_data["orcamento"],
        status=StatusTrabalho(int(form_data["status"])),
    )


def _servico_do_formulario(form_data, trabalho: Trabalho) -> Servico:
    return Servico(
        id=trabalho.id,
        metodologia=form_data["metodologia"],
        ferramenta=form_data["ferramenta"],
        trabalho=trabalho,
    )


def _demanda_do_formulario(form_data, trabalho: Trabalho) -> Demanda:
    return Demanda(
        id=trabalho.id,
        exigencias=form_data["exigencias"],
        prazo=form_data["prazo"],
        trabalho=trabalho,
    )


def _proposta_do_formulario(form_data, id=None) -> Proposta:
    return Proposta(
        id=id,
        orcamento=form_data["orcamento"],
        apresentacao=form_data["apresentacao"],
        prazo=form_data["prazo"],
        exigencia=form_data["exigencia"],
        tipo=TipoProposta(int(form_data["tipo"])),
        status=StatusProposta(int(form_data["status"])),
    )


# ============================================================================
# Conversão de objetos de domínio para os dados iniciais do formulário
# ============================================================================
def _dados_trabalho(trabalho: Trabalho) -> dict:
    return {
        "id": trabalho.id,
        "titulo": trabalho.titulo,
        "descricao": trabalho.descricao,
        "orcamento": trabalho.orcamento,
        "status": trabalho.status.value,
    }


def _dados_servico(servico: Servico) -> dict:
    dados = _dados_trabalho(servico.trabalho)
    dados.update(metodologia=servico.metodologia, ferramenta=servico.ferramenta)
    return dados


def _dados_demanda(demanda: Demanda) -> dict:
    dados = _dados_trabalho(demanda.trabalho)
    dados.update(exigencias=demanda.exigencias, prazo=demanda.prazo)
    return dados


def _dados_proposta(proposta: Proposta) -> dict:
    return {
        "id": proposta.id,
        "orcamento": proposta.orcamento,
        "apresentacao": proposta.apresentacao,
        "prazo": proposta.prazo,
        "exigencia": proposta.exigencia,
        "tipo": proposta.tipo.value,
        "status": proposta.status.value,
    }


# ============================================================================
# Operações de cada CRUD (usam apenas os Repositories do core)
# ============================================================================
def _alias_bd() -> str:
    return ServicosFactory().obter_conexao_bd().DB_ALIAS


# ---- Trabalho
def _trabalho_incluir(form_data):
    ServicosFactory().obter_trabalho_repository().incluir(_trabalho_do_formulario(form_data))


def _trabalho_alterar(form_data):
    id = _id_do_formulario(form_data)
    ServicosFactory().obter_trabalho_repository().alterar(_trabalho_do_formulario(form_data, id))


def _trabalho_excluir(id):
    repo = ServicosFactory().obter_trabalho_repository()
    trabalho = repo.obter_por_id(id)
    if trabalho is None:
        raise ValueError("Trabalho não encontrado.")
    repo.excluir(trabalho)


# ---- Serviço (grava o Trabalho e o Serviço na mesma transação)
def _servico_incluir(form_data):
    fabrica = ServicosFactory()
    with transaction.atomic(using=_alias_bd()):
        trabalho = fabrica.obter_trabalho_repository().incluir(_trabalho_do_formulario(form_data))
        fabrica.obter_servico_repository().incluir(_servico_do_formulario(form_data, trabalho))


def _servico_alterar(form_data):
    fabrica = ServicosFactory()
    id = _id_do_formulario(form_data)
    with transaction.atomic(using=_alias_bd()):
        trabalho = fabrica.obter_trabalho_repository().alterar(_trabalho_do_formulario(form_data, id))
        fabrica.obter_servico_repository().alterar(_servico_do_formulario(form_data, trabalho))


def _servico_excluir(id):
    ServicosFactory().obter_servico_repository().excluir(id)


# ---- Demanda (grava o Trabalho e a Demanda na mesma transação)
def _demanda_incluir(form_data):
    fabrica = ServicosFactory()
    with transaction.atomic(using=_alias_bd()):
        trabalho = fabrica.obter_trabalho_repository().incluir(_trabalho_do_formulario(form_data))
        fabrica.obter_demanda_repository().incluir(_demanda_do_formulario(form_data, trabalho))


def _demanda_alterar(form_data):
    fabrica = ServicosFactory()
    id = _id_do_formulario(form_data)
    with transaction.atomic(using=_alias_bd()):
        trabalho = fabrica.obter_trabalho_repository().alterar(_trabalho_do_formulario(form_data, id))
        fabrica.obter_demanda_repository().alterar(_demanda_do_formulario(form_data, trabalho))


def _demanda_excluir(id):
    repo = ServicosFactory().obter_demanda_repository()
    demanda = repo.obter_por_id(id)
    if demanda is None:
        raise ValueError("Demanda não encontrada.")
    repo.excluir(demanda)


# ---- Proposta
def _proposta_incluir(form_data):
    ServicosFactory().obter_proposta_repository().incluir(_proposta_do_formulario(form_data))


def _proposta_alterar(form_data):
    id = _id_do_formulario(form_data)
    ServicosFactory().obter_proposta_repository().alterar(_proposta_do_formulario(form_data, id))


def _proposta_excluir(id):
    repo = ServicosFactory().obter_proposta_repository()
    proposta = repo.obter_por_id(id)
    if proposta is None:
        raise ValueError("Proposta não encontrada.")
    repo.excluir(proposta)


# ============================================================================
# Tratamento comum dos CRUDs: listar, incluir, alterar, excluir e salvar
# ============================================================================
def _tratar_crud(request, acao, id, cfg):
    try:
        # define a classe de serviço
        servico = cfg["repository"]()

        # Listar registros
        # '<recurso>/': Exibir a pagina de listagem
        if acao is None:
            registros = servico.listar()
            return render(request, cfg["listar"], context={"registros": registros})

        # Salvar registro
        # '<recurso>/salvar/': insere, altera ou exclui um registro
        elif acao == "salvar":
            if request.method != "POST":
                raise Exception("Ação inválida")
            form_data = request.POST
            acao_form = form_data["acao"]

            try:
                if acao_form == "Inclusão":
                    cfg["incluir"](form_data)
                elif acao_form == "Exclusão":
                    cfg["excluir"](int(form_data["id"]))
                else:
                    cfg["alterar"](form_data)

                # Sempre retornar um HttpResponseRedirect após processar dados "POST".
                # Isso evita que os dados sejam postados 2 vezes caso usuário clicar "Voltar".
                return HttpResponseRedirect(reverse(cfg["rota"]))

            # se ocorreu algum erro, insere a mensagem para ser exibida no contexto da página
            except Exception as err:
                return render(
                    request,
                    cfg["editar"],
                    context={
                        "acao": acao_form,
                        "form": cfg["form"](data=form_data),
                        "ERRO": err,
                    },
                )

        # inserir registro
        # '<recurso>/incluir/': Exibir a pagina de inclusão
        elif acao == "incluir":
            return render(
                request, cfg["editar"], context={"acao": "Inclusão", "form": cfg["form"]()}
            )

        # Alterar ou excluir registro
        # '<recurso>/alterar/<:id>/': Exibir a pagina de alteração
        # '<recurso>/excluir/<:id>/': Exibir a pagina de exclusão
        elif acao in ["alterar", "excluir"]:
            acao = "Alteração" if acao == "alterar" else "Exclusão"

            # seleciona o registro pelo id informado
            registro = servico.obter_por_id(id)
            if registro is None:
                raise Exception("Registro não encontrado.")
            form = cfg["form"](cfg["dados_form"](registro))

            return render(request, cfg["editar"], context={"acao": acao, "form": form})

        # acao INVALIDA
        else:
            raise Exception("Ação inválida")

    # se ocorreu algum erro, insere a mensagem para ser exibida no contexto da página
    except Exception as err:
        return render(request, "home.html", context={"ERRO": err})


# Método responsavel por listar, incluir, alterar e excluir os Trabalhos.
def trabalhos(request, acao=None, id=None):
    return _tratar_crud(
        request,
        acao,
        id,
        {
            "rota": "trabalhos",
            "repository": lambda: ServicosFactory().obter_trabalho_repository(),
            "form": TrabalhoForm,
            "dados_form": _dados_trabalho,
            "listar": "trabalhos_listar.html",
            "editar": "trabalhos_editar.html",
            "incluir": _trabalho_incluir,
            "alterar": _trabalho_alterar,
            "excluir": _trabalho_excluir,
        },
    )


# Método responsavel por listar, incluir, alterar e excluir os Serviços.
def servicos(request, acao=None, id=None):
    return _tratar_crud(
        request,
        acao,
        id,
        {
            "rota": "servicos",
            "repository": lambda: ServicosFactory().obter_servico_repository(),
            "form": ServicoForm,
            "dados_form": _dados_servico,
            "listar": "servicos_listar.html",
            "editar": "servicos_editar.html",
            "incluir": _servico_incluir,
            "alterar": _servico_alterar,
            "excluir": _servico_excluir,
        },
    )


# Método responsavel por listar, incluir, alterar e excluir as Demandas.
def demandas(request, acao=None, id=None):
    return _tratar_crud(
        request,
        acao,
        id,
        {
            "rota": "demandas",
            "repository": lambda: ServicosFactory().obter_demanda_repository(),
            "form": DemandaForm,
            "dados_form": _dados_demanda,
            "listar": "demandas_listar.html",
            "editar": "demandas_editar.html",
            "incluir": _demanda_incluir,
            "alterar": _demanda_alterar,
            "excluir": _demanda_excluir,
        },
    )


# Método responsavel por listar, incluir, alterar e excluir as Propostas.
def propostas(request, acao=None, id=None):
    return _tratar_crud(
        request,
        acao,
        id,
        {
            "rota": "propostas",
            "repository": lambda: ServicosFactory().obter_proposta_repository(),
            "form": PropostaForm,
            "dados_form": _dados_proposta,
            "listar": "propostas_listar.html",
            "editar": "propostas_editar.html",
            "incluir": _proposta_incluir,
            "alterar": _proposta_alterar,
            "excluir": _proposta_excluir,
        },
    )


# Exibe a página inicial da aplicação
def home(request):
    """Exibe a pagina inicial da aplicação"""
    return render(request, "home.html")
