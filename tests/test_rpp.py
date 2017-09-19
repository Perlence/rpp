from decimal import Decimal
from os import path
from uuid import UUID

import attr
import pytest

from rpp import Element, loads, dumps
from rpp.encoder import tostr


def test_loads():
    src = """\
<REAPER_PROJECT 0.1 "4.32" 1372525904
  RIPPLE 0
  GROUPOVERRIDE 0 0 0
  AUTOXFADE 1
  <RECORD_CFG
    Y2FsZhAAAAAIAAAA
  >
  <RECORD_CFG
  >
  <VST "VST: ReaComp (Cockos)" reacomp.dll 0 "" 1919247213
    bWNlcu9e7f4EAAAAAQAAAAAAAAACAAAAAAAAAAQAAAAAAAAACAAAAAAAAAACAAAAAQAAAAAAAAACAAAAAAAAAFQAAAAAAAAAAAAQAA==
    776t3g3wrd7L/6o+AAAAAKabxDsK16M8AAAAAAAAAAAAAIA/AAAAAAAAAAAAAAAAnNEHMwAAgD8AAAAAzcxMPQAAAAAAAAAAAAAAAAAAAAAAAAAA
    AAAQAAAA
  >
  <SOURCE MIDI
    E 3840 b0 7b 00
  >
  <JS loser/3BandEQ ""
    0.000000 200.000000 0.000000 2000.000000 0.000000 0.000000 - - - - -
  >
>"""
    expected = Element('REAPER_PROJECT', (Decimal('0.1'), '4.32', 1372525904), [
        Element('RIPPLE', (0,)),
        Element('GROUPOVERRIDE', (0, 0, 0)),
        Element('AUTOXFADE', (1,)),
        Element('RECORD_CFG', (), ['Y2FsZhAAAAAIAAAA']),
        Element('RECORD_CFG', (), []),
        Element('VST', ('VST: ReaComp (Cockos)', 'reacomp.dll', 0, '', 1919247213), [
            'bWNlcu9e7f4EAAAAAQAAAAAAAAACAAAAAAAAAAQAAAAAAAAACAAAAAAAAAACAAAAAQAAAAAAAAACAAAAAAAAAFQAAAAAAAAAAAAQAA==',
            '776t3g3wrd7L/6o+AAAAAKabxDsK16M8AAAAAAAAAAAAAIA/AAAAAAAAAAAAAAAAnNEHMwAAgD8AAAAAzcxMPQAAAAAAAAAAAAAAAAAAAAAAAAAA',
            'AAAQAAAA',
        ]),
        Element('SOURCE', ('MIDI',), [
            Element('E', (3840, 'b0', '7b', '00')),
        ]),
        Element('JS', ('loser/3BandEQ', ''), [(
            Decimal('0.000000'), Decimal('200.000000'), Decimal('0.000000'), Decimal('2000.000000'),
            Decimal('0.000000'), Decimal('0.000000'), None, None, None, None, None,
        )]),
    ])
    assert attr.astuple(loads(src)) == attr.astuple(expected)


def test_tostr():
    assert tostr('') == '""'
    assert tostr('Track') == 'Track'
    assert tostr('Track 1') == '"Track 1"'
    assert tostr('Track "1"') == '\'Track "1"\''
    assert tostr('Track "1" \'2\'') == '`Track "1" \'2\'`'
    assert tostr('Track "1" \'2\' `3`') == '`Track "1" \'2\' \'3\'`'
    assert tostr(UUID('010F6508-D16E-4DA0-BE44-E8F3C39D6314')) == '{010F6508-D16E-4DA0-BE44-E8F3C39D6314}'


def test_dumps():
    src = Element('ENTRY', (1, 2, 3), [
        Element('RIPPLE', (0,)),
        Element('SUBFOLDER', ('',), []),
        Element('RECORD_CFG', (), []),
        'AAAQAAAA',
    ])
    expected = """\
<ENTRY 1 2 3
  RIPPLE 0
  <SUBFOLDER ""
  >
  <RECORD_CFG
  >
  AAAQAAAA
>\n"""
    assert dumps(src) == expected


@pytest.mark.skip
def test_conversion():
    DIR = path.dirname(__file__)
    with open(path.join(DIR, '..', 'data', 'vst.RPP')) as fp:
        raw_proj = fp.read()
    proj = loads(raw_proj)
    raw_proj2 = dumps(proj)
    with open(path.join(DIR, '..', 'data', 'vst2.RPP'), 'w') as fp:
        fp.write(raw_proj2)
    assert raw_proj2 == raw_proj
