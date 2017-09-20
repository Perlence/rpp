from ply import yacc

from .element import Element
from .scanner import tokens  # noqa


def parser():
    return yacc.yacc(optimize=True, debug=False, write_tables=True)


def p_tree(t):
    """tree : OPEN root CLOSE NEWLINE
            | OPEN root items CLOSE NEWLINE"""
    t[0] = t[2]
    if len(t) > 5:
        t[0].extend(t[3])


def p_root(t):
    """root : STRING NEWLINE
            | STRING tuple NEWLINE"""
    t[0] = Element(t[1], children=[])
    if len(t) > 3:
        t[0].attrib = t[2]


def p_items(t):
    """items : item
             | item items"""
    if t[0] is None:
        t[0] = []
    t[0].append(t[1])
    if len(t) > 2:
        t[0] += t[2]


def p_item_element(t):
    """item : STRING tuple NEWLINE"""
    t[0] = Element(t[1], t[2])


def p_item_tuple(t):
    """item : tuple NEWLINE"""
    if len(t[1]) == 1:
        t[0] = t[1][0]
    else:
        t[0] = t[1]


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
             | STRING"""
    t[0] = t[1]


def p_error(t):
    if t is None:
        raise ValueError("Syntax error at EOF")
    message = "Syntax error at line %d, token=%s" % (t.lineno or 1, t.type)
    raise ValueError(message)
