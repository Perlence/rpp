import tokens
import syntax

def tokenize(string):
    tokens.lex.input(string)
    while True:
        tok = tokens.lex.token()
        if not tok: 
            break
        yield tok

def parse(*args, **kwargs):
    return syntax.yacc.parse(*args, **kwargs)
