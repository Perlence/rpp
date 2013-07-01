import scanner
import decoder
import encoder
from scanner import Symbol

def loads(string):
    return decoder.yacc.parse(string)

def load(fp):
    return loads(fp.read())

def dumps(lists):
    return encoder.encode(lists)

def dump(lists, fp):
    fp.write(dumps(lists))
