from django import forms
from app.factory import ServicosFactory

from app.rotulos import opcoes
from core.entities.proposta import StatusProposta, TipoProposta
from core.entities.trabalho import StatusTrabalho


class TrabalhoForm(forms.Form):
    id = forms.IntegerField(
        label="ID", widget=forms.TextInput(attrs={"readonly": "readonly"}), required=False
    )
    titulo = forms.CharField(label="Título", max_length=150, required=True)
    descricao = forms.CharField(
        label="Descrição", widget=forms.Textarea(attrs={"rows": 4, "cols": 40}), required=True
    )
    orcamento = forms.CharField(label="Orçamento", max_length=50, required=True)
    status = forms.ChoiceField(
        label="Status", choices=opcoes(StatusTrabalho), required=True
    )


class ServicoForm(TrabalhoForm):
    metodologia = forms.CharField(label="Metodologia", max_length=200, required=True)
    ferramenta = forms.CharField(label="Ferramenta", max_length=200, required=True)


class DemandaForm(TrabalhoForm):
    exigencias = forms.CharField(
        label="Exigências", widget=forms.Textarea(attrs={"rows": 3, "cols": 40}), required=True
    )
    prazo = forms.CharField(label="Prazo", max_length=50, required=True)


class PropostaForm(forms.Form):
    trabalho_id = forms.ChoiceField(label="Trabalho", required=True)
    id = forms.IntegerField(
        label="ID", widget=forms.TextInput(attrs={"readonly": "readonly"}), required=False
    )
    orcamento = forms.CharField(label="Orçamento", max_length=50, required=True)
    apresentacao = forms.CharField(
        label="Apresentação", widget=forms.Textarea(attrs={"rows": 4, "cols": 40}), required=True
    )
    prazo = forms.CharField(label="Prazo", max_length=50, required=True)
    exigencia = forms.CharField(
        label="Exigência", widget=forms.Textarea(attrs={"rows": 3, "cols": 40}), required=True
    )
    tipo = forms.ChoiceField(label="Tipo", choices=opcoes(TipoProposta), required=True)
    status = forms.ChoiceField(label="Status", choices=opcoes(StatusProposta), required=True)

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            fabrica = ServicosFactory()
            servicos = fabrica.obter_servico_repository().listar()
            demandas = fabrica.obter_demanda_repository().listar()

            self._ids_servico = {str(s.id) for s in servicos}
            self._ids_demanda = {str(d.id) for d in demandas}
            self.fields["trabalho_id"].choices = (
                [(s.id, f"[Serviço] {s.trabalho.titulo}") for s in servicos]
                + [(d.id, f"[Demanda] {d.trabalho.titulo}") for d in demandas]
            )
