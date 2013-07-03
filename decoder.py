from ply import yacc
from scanner import tokens

class RPP(list):
    def __repr__(self):
        return "RPP(%s)" % list.__repr__(self)

    def findall(self, name):
        '''Find all elements that start with given name
        '''
        for i, x in enumerate(self):
            if isinstance(x, RPP):
                for y in x.findall(name):
                    yield [i] + y
            elif x[0] == name:
                yield [i, x]

    def find(self, name):
        '''Find first element that starts with given name

        :returns: List where first elements are indexes and the last is the found value.

        >>> l = RPP([['NAME', 1, 2], RPP([['NUN', 1, 5.234, 'x']]), RPP([['SUS', 3]])])
        >>> l.find('SUS')
        [2, 0, ['SUS', 3]]
        '''
        try:
            return self.findall(name).next()
        except StopIteration:
            return None

    def update(self, *args):
        '''Traverse the list using given indexes and change the value

        :param *indexes: list of indexes
        :param value:    new value

        >>> l = RPP([['NAME', 1, 2], RPP([['NUN', 1, 5.234, 'x']]), RPP([['SUS', 3]])])
        >>> l.update(1, 0, ['LUL', 42])
        >>> l
        RPP([['NAME', 1, 2], RPP([['LUL', 42]]), RPP([['SUS', 3]])])
        '''
        getindexes, setindex, value = args[:-2], args[-2], args[-1]
        level = self
        for i in getindexes:
            level = level[i]
        level[setindex] = value


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
             | SYMBOL'''
    t[0] = t[1]

def p_error(t):
    message = "Syntax error at line %d, token=%s" % (t.lineno or 0, t.type)
    raise ValueError(message)

yacc.yacc()
