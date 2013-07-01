import scanner
import decoder

def loads(string):
    return decoder.yacc.parse(string)

def load(fp):
    return decoder.yacc.parse(fp.read())
