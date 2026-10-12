from django import template

from app.rotulos import ROTULOS

register = template.Library()


@register.filter
def rotulo(valor):
    """Exibe o texto amigável de um Enum do domínio."""
    return ROTULOS.get(valor, valor)
