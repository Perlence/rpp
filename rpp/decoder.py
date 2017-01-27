from ply import yacc
from .scanner import *

class RPP(list):
    def __repr__(self):
        return "RPP(%s)" % list.__repr__(self)

    def findall(self, name, location = None):
        '''Find all elements that start with given name

        :returns: generator of tuples with first element as list of tree indexes 
                  and the second as the found value.

        >>> l = RPP([['NAME', 1, 2], RPP([['NUN', 1, 5.234, 'x']]), RPP([['SUS', 3]])])
        >>> list(l.findall('SUS'))
        [([2, 0], ['SUS', 3]])]
        '''
        for i, x in enumerate(self):
            if x[0] == name:
                if location is None:
                    yield [i], x
                else:
                    yield location + [i], x
            elif isinstance(x, RPP):
                js, y = x.findall(name, location = [i])
                yield location + js, y

    def find(self, name):
        '''Find first element that starts with given name
        '''
        return next(self.findall(name), None)

    def update(self, indexes, value):
        '''Traverse the list using given indexes and change the value

        :param indexes:  list of indexes
        :param value:    new value

        >>> l = RPP([['NAME', 1, 2], RPP([['NUN', 1, 5.234, 'x']]), RPP([['SUS', 3]])])
        >>> l.update([1, 0], ['LUL', 42])
        >>> l
        RPP([['NAME', 1, 2], RPP([['LUL', 42]]), RPP([['SUS', 3]])])
        '''
        lastindex = indexes.pop(-1)
        level = self
        for i in indexes:
            level = level[i]
        level[lastindex] = value


def p_tree(t):
    '''tree : OPEN items CLOSE'''
    t[0] = t[2]

def p_items(t):
    '''items : item
             | item items'''
    if t[0] is None:
        t[0] = RPP([])
    t[0].append(t[1])
    if len(t) > 2:
        t[0] += t[2]

def p_item_novalue(t):
    '''item : NAME'''
    t[0] = RPP([t[1]])

def p_item_list(t):
    '''item : NAME list'''
    if t[1] == 'E':
        int_, hexes = t[2][0], t[2][1:]
        hexes = [Hex(str(x)) for x in hexes]
        t[0] = RPP([t[1]]) + [int_] + hexes
    else:
        t[0] = RPP([t[1]]) + t[2]

def p_item_tree(t):
    '''item : tree'''
    t[0] = t[1]

def p_list(t):
    '''list : value
            | value list'''
    if t[0] is None:
        t[0] = RPP([])
    t[0].append(t[1])
    if len(t) > 2:
        t[0] += t[2]

def p_value(t):
    '''value : NULL 
             | INT 
             | FLOAT
             | STRING
             | UUID
             | SYMBOL
             | FORMAT
             | CHUNK'''
    t[0] = t[1]

def p_error(t):
    message = "Syntax error at line %d, token=%s" % (t.lineno or 0, t.type)
    raise ValueError(message)

yacc.yacc(optimize=True, debug=False, write_tables=False)
