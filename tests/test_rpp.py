from os import path

import attr
import pytest

from rpp import Element, loads, dumps
from rpp.scanner import Lexer
from rpp.encoder import encode_value


def test_scanner():
    lex = Lexer()
    lex.input('<REAPER - 5 05 0.5 "4.32"\n>')
    assert [tok.value for tok in lex] == [
        '<', 'REAPER', '-', '5', '05', '0.5', '4.32', '\n', '>', '\n',
    ]

    lex.input('<"REAPER"\n>')
    assert [tok.value for tok in lex] == [
        '<', '"REAPER"', '\n', '>', '\n',
    ]

    lex.input("""\
<NOTES
  |beep  boop
  |
  |hello world
  |0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~
>""")
    assert [tok.value for tok in lex] == [
        '<', 'NOTES', '\n',
        '|beep  boop', '\n',
        '|', '\n',
        '|hello world', '\n',
        '|0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~', '\n',
        '>', '\n',
    ]

    lex.input('<REAPER "BEEP\n>')
    with pytest.raises(ValueError) as exc:
        list(lex)
    assert 'closing quote not found at line 1' in str(exc)


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
    e 3840 b0 7b 00
  >
  <JS loser/3BandEQ ""
    0.000000 200.000000 0.000000 2000.000000 0.000000 0.000000 - - - - -
  >
  NAME 09azAZ!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~
  NAME `09 azAZ!"#$%&'()*+,-./:;<=>?@[\\]^_'{|}~`
  NAME <
  NAME >
  NAME <>
  VERSION 4.32
>"""
    expected = Element('REAPER_PROJECT', ['0.1', '4.32', '1372525904'], [
        ['RIPPLE', '0'],
        ['GROUPOVERRIDE', '0', '0', '0'],
        ['AUTOXFADE', '1'],
        Element('RECORD_CFG', [], ['Y2FsZhAAAAAIAAAA']),
        Element('RECORD_CFG', [], []),
        Element('VST', ['VST: ReaComp (Cockos)', 'reacomp.dll', '0', '', '1919247213'], [
            'bWNlcu9e7f4EAAAAAQAAAAAAAAACAAAAAAAAAAQAAAAAAAAACAAAAAAAAAACAAAAAQAAAAAAAAACAAAAAAAAAFQAAAAAAAAAAAAQAA==',
            '776t3g3wrd7L/6o+AAAAAKabxDsK16M8AAAAAAAAAAAAAIA/AAAAAAAAAAAAAAAAnNEHMwAAgD8AAAAAzcxMPQAAAAAAAAAAAAAAAAAAAAAAAAAA',  # noqa
            'AAAQAAAA',
        ]),
        Element('SOURCE', ['MIDI'], [
            ['E', '3840', 'b0', '7b', '00'],
            ['e', '3840', 'b0', '7b', '00'],
        ]),
        Element('JS', ['loser/3BandEQ', ''], [
            ['0.000000', '200.000000', '0.000000', '2000.000000', '0.000000', '0.000000', '-', '-', '-', '-', '-'],
        ]),
        ['NAME', '09azAZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'],
        ['NAME', '09 azAZ!"#$%&\'()*+,-./:;<=>?@[\\]^_\'{|}~'],
        ['NAME', '<'],
        ['NAME', '>'],
        ['NAME', '<>'],
        ['VERSION', '4.32'],
    ])
    actual = loads(src)
    assert attr.asdict(actual) == attr.asdict(expected)


def test_tostr():
    assert encode_value('') == '""'
    assert encode_value('"hey') == "'\"hey'"
    assert encode_value('Track') == 'Track'
    assert encode_value('Track 1') == '"Track 1"'
    assert encode_value('Track "1"') == '\'Track "1"\''
    assert encode_value('Track "1" \'2\'') == '`Track "1" \'2\'`'
    assert encode_value('Track "1" \'2\' `3`') == '`Track "1" \'2\' \'3\'`'
    assert encode_value('{010F6508-D16E-4DA0-BE44-E8F3C39D6314}') == '{010F6508-D16E-4DA0-BE44-E8F3C39D6314}'


def test_dumps():
    src = Element('ENTRY', ('1', '2', '3'), [
        ['RIPPLE', 0],
        Element('SUBFOLDER', ('',)),
        Element('RECORD_CFG', ()),
        ['NAME', '09azAZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'],
        ['NAME', '09 azAZ!"#$%&\'()*+,-./:;<=>?@[\\]^_\'{|}~'],
        ['VERSION', '4.32'],
        ['NAME', '|Beep boop'],
        'AAAQAAAA',
    ])
    expected = """\
<ENTRY 1 2 3
  RIPPLE 0
  <SUBFOLDER ""
  >
  <RECORD_CFG
  >
  NAME 09azAZ!"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~
  NAME `09 azAZ!"#$%&'()*+,-./:;<=>?@[\\]^_'{|}~`
  VERSION 4.32
  NAME "|Beep boop"
  AAAQAAAA
>\n"""
    assert dumps(src) == expected


@pytest.mark.parametrize('filename', [
    'empty.RPP',
    'vst.RPP',
])
def test_conversion(filename):
    DIR = path.dirname(__file__)
    with open(path.join(DIR, 'data', filename)) as fp:
        raw_proj = fp.read()

    # Allow some differences
    raw_proj = (raw_proj
                .replace('"4.32"', '4.32')
                .replace('"5.50c"', '5.50c')
                .replace('"audio/"', 'audio/')
                .replace("'{1EB4F5A8-25D1-43CA-91D1-F1CA4ED005ED}'", '{1EB4F5A8-25D1-43CA-91D1-F1CA4ED005ED}')
                .replace("'{35FAE399-C558-4F4A-903F-4FF6F0470B4D}'", '{35FAE399-C558-4F4A-903F-4FF6F0470B4D}')
                .replace('"Trackk"', 'Trackk')
                .replace("''", '""')
                .replace('- \n', '-\n'))

    proj = loads(raw_proj)
    raw_proj2 = dumps(proj)
    assert raw_proj2 == raw_proj
    assert loads(raw_proj2) == proj
