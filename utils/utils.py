def filter_price(val):
    return f'R$ {val:.2f}'.replace('.', ',')


def cart_qtd_total(carrinho):
    return sum([item['quantidade'] for item in carrinho.values()])


def cart_totals(carrinho):
    total = 0
    for c in carrinho.values():
        preco_1 = c['preco_quantitativo_promocional']
        preco_2 = c['preco_quantitativo']

        if preco_1:
            total += preco_1
        else:
            total += preco_2
    return total

    # return sum(
    #     [
    #         item.get('preco_quantitativo_promocional')
    #         if item.get('preco_quantitativo_promocional')
    #         else item.get('preco_quantitativo')
    #         for item in carrinho.values()
    #     ]
    # )
