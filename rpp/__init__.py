"""RPP is a format used to describe `REAPER <http://reaper.fm>`_
projects."""

from .element import Element
from .rpp import dump, dumps, loads, load


__version__ = '0.5'
__author__ = 'Sviatoslav Abakumov <dust.harvesting@gmail.com>'
__all__ = ['dump', 'dumps', 'load', 'loads', 'Element']
