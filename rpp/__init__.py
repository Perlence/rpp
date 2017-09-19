"""RPP is a format used to describe REAPER <http://reaper.fm> projects."""

from ply import yacc

from . import scanner
from .decoder import Element
from .encoder import encode


__version__ = '0.1'
__all__ = ['dump', 'dumps', 'load', 'loads', 'Element']
__author__ = 'Sviatoslav Abakumov <dust.harvesting@gmail.com>'


def loads(string):
    lexer = scanner.lexer()
    return yacc.parse(string.strip(), lexer)


def load(fp):
    return loads(fp.read())


def dumps(lists, indent=2):
    return encode(lists, indent=indent)


def dump(lists, fp, indent=2):
    fp.write(dumps(lists, indent))
