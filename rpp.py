import uuid

tokens = (
    # 'WHITESPACE', 
    'OPEN',
    'CLOSE',
    'NULL',
    'NAME',
    'SYMBOL',
    'STRING',
    'UUID',
    'FLOAT',
    'INT',
    )

# Tokens

# t_BASE64 = r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?'
# t_BASE64 = r'^(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})$'
t_SYMBOL = r'[a-zA-Z0-9_+/:=]+'
t_OPEN   = r'<'
t_CLOSE  = r'>'

def t_NAME(t):
    r'[A-Z][A-Z0-9_]*(?=\s+)'
    return t

def t_UUID(t):
    r"(?P<quote>(?:'?))\{[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\}(?P=quote)"
    t.value = uuid.UUID(t.value.strip("'"))
    return t

def t_STRING(t):
    r'(?:"([^"]*)")|(?:\'([^\']*)\')'
    t.value = t.value.strip('"')
    return t

def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'-?\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_NULL(t):
    r'-'
    t.value = None
    return t

# Ignored characters
t_ignore = ' \t'

def t_newline(t): 
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

import ply.lex as lex
lexer = lex.lex()

