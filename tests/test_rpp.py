from decimal import Decimal

from rpp import RPP, Symbol, loads, dumps


def test_rpp_findall():
    l = RPP([['NAME', 1, 2], RPP([['NUN', 1, 5.234, 'x']]), RPP([['SUS', 3]])])
    assert list(l.findall('SUS')) == [([2, 0], ['SUS', 3])]


def test_rpp_update():
    l = RPP([['NAME', 1, 2], RPP([['NUN', 1, 5.234, 'x']]), RPP([['SUS', 3]])])
    l.update([1, 0], ['LUL', 42])
    assert l == RPP([['NAME', 1, 2], RPP([['LUL', 42]]), RPP([['SUS', 3]])])


def test_symbol():
    src = '<VST "VSTi: Oddity 2 (GForce)" Oddity2_x64_linux.so 0 "" 1330603058>'
    expected = RPP([['VST', 'VSTi: Oddity 2 (GForce)', Symbol('Oddity2_x64_linux.so'), 0, '', 1330603058]])
    assert loads(src) == expected


def test_loads():
    src = """\
<REAPER_PROJECT 0.1 "4.32" 1372525904
  RIPPLE 0
  GROUPOVERRIDE 0 0 0
  AUTOXFADE 1
  <RECORD_CFG
    Y2FsZhAAAAAIAAAA
  >
>"""
    expected = RPP([['REAPER_PROJECT', Decimal('0.1'), '4.32', 1372525904],
                    ['RIPPLE', 0],
                    ['GROUPOVERRIDE', 0, 0, 0],
                    ['AUTOXFADE', 1],
                    RPP([['RECORD_CFG', Symbol('Y2FsZhAAAAAIAAAA')]])])
    assert loads(src) == expected


def test_dumps():
    src = [['ENTRY', 1, 2, 3], [['SUBFOLDER', '']]]
    expected = '<ENTRY 1 2 3\n  <SUBFOLDER ""\n  >\n>'
    assert dumps(src) == expected
