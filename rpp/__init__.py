r"""RPP is a format used to describe REAPER <http://reaper.fm> projects.

Decoding RPP::

    >>> import rpp
    >>> rpp.loads('<REAPER_PROJECT 0.1 "4.32" 1372525904\nRIPPLE 0 GROUPOVERRIDE 0 0 0\nAUTOXFADE 1>')
    RPP([['REAPER_PROJECT', 0.1, '4.32', 1372525904], ['RIPPLE', 0], ['GROUPOVERRIDE', 0, 0, 0], ['AUTOXFADE', 1]])

Encoding RPP::

    >>> import rpp
    >>> rpp.dumps([['ENTRY', 1, 2, 3], [['SUBFOLDER', '']]])
    '<ENTRY 1 2 3\n  <SUBFOLDER ""\n  >\n>\n'
"""
__version__ = '0.1'
__all__ = [
    'dump', 'dumps', 'load', 'loads',
    'RPP', 'Symbol',
    ]

__author__ = 'Sviatoslav Abakumov <dust.harvesting@gmail.com>'

from scanner import Symbol
from decoder import RPP, yacc
from encoder import encode

def loads(string):
    return decoder.yacc.parse(string)

def load(fp):
    return loads(fp.read())

def dumps(lists):
    return encoder.encode(lists)

def dump(lists, fp):
    fp.write(dumps(lists))
