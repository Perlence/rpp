from uuid import UUID
from decimal import Decimal
import re
import base64
from ply import lex

p = re.compile(r' +')

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


class Chunk(object):
    def __init__(self, c):
        self.base64_value = p.sub('', c).translate(None, '\r\n')

    def __repr__(self):
        return 'Chunk(%s)' % self.value

    def __str__(self):
        return self.value

    @property
    def value(self):
        return self.base64_value
    
    @property
    def binary_value(self):
        return base64.b64decode(self.base64_value)

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
    'CHUNK',
    'SYMBOL'
    )

t_OPEN   = r'<'
t_CLOSE  = r'>'

# FORMAT should come before NAME so it is matched ahead of a Name.
def t_FORMAT(t):
    r'(WAV|WAVE|AIFF|APE|DDP|FLAC|MP3|OGG|WAVPACK|MIDI)(?=\s+)'
    t.value = Format(t.value)
    return t

# The imbeciles at Reaper write 'TRACK' 'NAME' entries with or without quotes depending on whether
# there is a space in the string. This is insane and makes parsing unbelievably difficult:
# some 'NAME' items will be scanned as STRING, others will be SYMBOLs, or NAMEs.
# To try to work around this, we try to catch this context sensitive case and ultimately
# generate a STRING token.
def t_BOGUSSTRING(t):
    r'(?<=NAME\s)(?:([^"\'\s]+))(?=\s+)'
    t.type = 'STRING'
    return t

def t_NAME(t):
    r'[A-Z][A-Z0-9_]*(?=\s+)'
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
    r'-?\d+\.\d+(?=\s+)'
    t.value = Decimal(t.value)
    return t

def t_INT(t):
    r'-?\d+(?=\s+)'
    t.value = int(t.value)
    return t

def t_NULL(t):
    r'-(?=\s+)'
    t.value = None
    return t

def t_CHUNK(t):
    r'([a-zA-Z0-9+/:=]+\s+)+(?=>)'
    # Update the line number count since we swallow newlines inside a chunk.
    t.lexer.lineno += t.value.count('\n')
    t.value = Chunk(t.value)
    return t

def t_SYMBOL(t):
    r'[\w+:={}\-\./\(\)]+'
    t.value = Symbol(t.value)
    return t

# Ignored characters
t_ignore = ' \t'

def t_newline(t):
    r'[\r\n]+'
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
            break      # No more input
        yield tok
