"""RPP is a format used to describe REAPER <http://reaper.fm> projects."""

from . import scanner
from .decoder import parser
from .element import Element
from .encoder import encode


__version__ = '0.1'
__author__ = 'Sviatoslav Abakumov <dust.harvesting@gmail.com>'
__all__ = ['dump', 'dumps', 'load', 'loads', 'Element']


def loads(string):
    lexer = scanner.lexer()
    yacc = parser()
    return yacc.parse(string.strip(), lexer)


def load(fp):
    return loads(fp.read())


def dumps(lists, indent=2):
    return encode(lists, indent=indent)


def dump(lists, fp, indent=2):
    fp.write(dumps(lists, indent))
