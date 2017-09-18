from uuid import UUID
from decimal import Decimal

from ply import lex


class Hex(object):
    def __init__(self, x):
        self.value = int(x, 16)

    def __int__(self):
        return self.value

    def __repr__(self):
        return "Hex('%s')" % hex(self.value)

    def __str__(self):
        return hex(self.value).lstrip('0x').zfill(2)


class Format(str):
    def __repr__(self):
        return 'Format(%s)' % str.__repr__(self)


class Symbol(str):
    def __repr__(self):
        return 'Symbol(%s)' % str.__repr__(self)


tokens = (
    'OPEN',
    'CLOSE',
    'FORMAT',
    'NAME',
    'UUID',
    'STRING',
    'FLOAT',
    'INT',
    'NULL',
    'SYMBOL',
    )

t_OPEN = r'<'
t_CLOSE = r'>'


def t_FORMAT(t):
    r"(WAV|AIFF|APE|DDP|FLAC|MP3|OGG|WAVPACK|MIDI)(?=\s+)"
    t.value = Format(t.value)
    return t


def t_NAME(t):
    r"[A-Z][A-Z0-9_]*(?=\s+)"
    return t


def t_UUID(t):
    r"\{[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\}(?=\s+)"
    t.value = UUID(t.value.strip("'"))
    return t


def t_STRING(t):
    r'(?:"([^"]*)")|(?:\'([^\']*)\')(?=\s+)'
    if t.value[0] == '"':
        t.value = t.value.strip('"')
    else:
        t.value = t.value.strip("'")
    return t


def t_FLOAT(t):
    r"-?\d+\.\d+(?=\s+)"
    t.value = Decimal(t.value)
    return t


def t_INT(t):
    r"-?\d+(?=\s+)"
    t.value = int(t.value)
    return t


def t_NULL(t):
    r"-(?=\s+)"
    t.value = None
    return t


def t_SYMBOL(t):
    r"[a-zA-Z0-9_+/:=]+"
    t.value = Symbol(t.value)
    return t


# Ignored characters
t_ignore = ' \t'


def t_newline(t):
    r"[\r\n]+"
    t.lexer.lineno += len(t.value.splitlines())


def t_error(t):
    s = t.lexer.lexdata[t.lexer.lexpos:]
    message = "Scanning error. Illegal character '%s' at line %d" % (t.value[0], t.lineno or 0)
    raise lex.LexError(message, s)


lex.lex(optimize=False, debug=False)


def tokenize(string):
    lex.input(string)
    while True:
        tok = lex.token()
        if not tok:
            break
        yield tok
