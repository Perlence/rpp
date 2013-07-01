from tokens import tokens

def p_tree(t):
    '''tree : OPEN items CLOSE'''
    t[0] = t[2]

def p_items(t):
    '''items : item
             | item items'''
    if t[0] is None:
        t[0] = []
    t[0].append(t[1])
    if len(t) > 2:
        t[0] += t[2]

def p_item_novalue(t):
    '''item : NAME'''
    t[0] = [t[1]]

def p_item_list(t):
    '''item : NAME list'''
    t[0] = [t[1]] + t[2]

def p_item_tree(t):
    '''item : tree'''
    t[0] = t[1]

def p_list(t):
    '''list : value
            | value list'''
    if t[0] is None:
        t[0] = []
    t[0].append(t[1])
    if len(t) > 2:
        t[0] += t[2]

def p_value(t):
    '''value : NULL 
             | INT 
             | FLOAT
             | STRING
             | UUID
             | SYMBOL'''
    t[0] = t[1]

def p_error(t):
    print("Syntax error on line %d at '%s'" % (t.lineno, t.value))

from ply import yacc
yacc.yacc()
