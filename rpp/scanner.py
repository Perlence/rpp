from decimal import Decimal

from ply import lex


def tokenize(string):
    lex = lexer()
    lex.input(string)
    while True:
        tok = lex.token()
        if not tok:
            break
        yield tok


def lexer():
    return lex.lex(optimize=False, debug=False)


tokens = (
    'OPEN',
    'CLOSE',
    'NULL',
    'INT',
    'FLOAT',
    'UUID',
    'STRING',
    'newline',
)

t_OPEN = r'<'
t_CLOSE = r'>'


def t_NULL(t):
    r"-(?=[ \t\n<>]+)"
    t.value = None
    return t


def t_INT(t):
    r"-?([0-9]|[1-9][0-9]+)(?=[ \t\n<>]+)"
    t.value = int(t.value)
    return t


def t_FLOAT(t):
    r"-?\d+\.\d+(?=[ \t\n<>]+)"
    t.value = Decimal(t.value)
    return t


def t_STRING(t):
    r'("([^"]*")|\'([^\']*)\'|`([^`]*)"|[a-zA-Z0-9{}_+-/:=.]+)(?=[ \t\n<>]+)'
    if t.value[0] == '"':
        t.value = t.value.strip('"')
    elif t.value[0] == "'":
        t.value = t.value.strip("'")
    elif t.value[0] == '`':
        t.value = t.value.strip('`')
    return t


t_ignore = ' \t'


def t_newline(t):
    r"[\r\n]+"
    t.lexer.lineno += len(t.value.splitlines())
    return t


def t_error(t):
    s = t.lexer.lexdata[t.lexer.lexpos:]
    message = "Scanning error. Illegal character '%s' at line %d" % (t.value[0], t.lineno or 0)
    raise lex.LexError(message, s)
