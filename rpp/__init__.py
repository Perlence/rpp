r"""RPP is a format used to describe REAPER <http://reaper.fm> projects.

Decoding RPP::

    >>> import rpp
    >>> rpp.loads('<REAPER_PROJECT 0.1 "4.32" 1372525904\nRIPPLE 0 GROUPOVERRIDE 0 0 0\nAUTOXFADE 1>')
    RPP([['REAPER_PROJECT', 0.1, '4.32', 1372525904], ['RIPPLE', 0], ['GROUPOVERRIDE', 0, 0, 0], ['AUTOXFADE', 1]])

Encoding RPP::

    >>> import rpp
    >>> rpp.dumps([['ENTRY', 1, 2, 3], [['SUBFOLDER', '']]])
    '<ENTRY 1 2 3\n  <SUBFOLDER ""\n  >\n>'
"""

from .scanner import Symbol
from .decoder import RPP, yacc  # noqa
from .encoder import encode  # noqa


__version__ = '0.1'
__all__ = ['dump', 'dumps', 'load', 'loads', 'RPP', 'Symbol']
__author__ = 'Sviatoslav Abakumov <dust.harvesting@gmail.com>'


def loads(string):
    return yacc.parse(string)


def load(fp):
    return loads(fp.read())


def dumps(lists, indent=2):
    return encode(lists, indent=indent)


def dump(lists, fp, indent=2):
    fp.write(dumps(lists, indent))
