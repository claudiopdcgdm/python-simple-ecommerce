from django.template import Library
from utils import utils

register = Library()


@register.filter
def filter_price(val):
    return utils.filter_price(val)


@register.filter
def cart_qtd_total(carrinho):
    return utils.cart_qtd_total(carrinho)


@register.filter
def cart_totals(carrinho):
    return utils.cart_totals(carrinho)
