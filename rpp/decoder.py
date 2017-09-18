from ply import yacc

from .scanner import Hex, tokens  # noqa


def p_tree(t):
    """tree : OPEN items CLOSE"""
    t[0] = t[2]


def p_items(t):
    """items : item
             | item items"""
    if t[0] is None:
        t[0] = []
    t[0].append(t[1])
    if len(t) > 2:
        t[0] += t[2]


def p_item_novalue(t):
    """item : NAME"""
    t[0] = (t[1],)


def p_item_tuple(t):
    """item : NAME tuple"""
    if t[1] == 'E':
        int_, hexes = t[2][0], t[2][1:]
        hexes = tuple(Hex(str(x)) for x in hexes)
        t[0] = (t[1], int_) + hexes
    else:
        t[0] = (t[1],) + t[2]


def p_item_tree(t):
    """item : tree"""
    t[0] = t[1]


def p_tuple(t):
    """tuple : value
             | value tuple"""
    if t[0] is None:
        t[0] = ()
    t[0] += (t[1],)
    if len(t) > 2:
        t[0] += t[2]


def p_value(t):
    """value : NULL
             | INT
             | FLOAT
             | STRING
             | UUID
             | SYMBOL
             | FORMAT"""
    t[0] = t[1]


def p_error(t):
    message = "Syntax error at line %d, token=%s" % (t.lineno or 0, t.type)
    raise ValueError(message)


yacc.yacc(optimize=True, debug=False, write_tables=False)
