from decimal import Decimal

from rpp import Symbol, loads, dumps


def test_symbol():
    src = '<VST "VSTi: Oddity 2 (GForce)" Oddity2_x64_linux.so 0 "" 1330603058>'
    expected = [('VST', 'VSTi: Oddity 2 (GForce)', Symbol('Oddity2_x64_linux.so'), 0, '', 1330603058)]
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
  <RECORD_CFG
  >
>"""
    expected = [('REAPER_PROJECT', Decimal('0.1'), '4.32', 1372525904),
                ('RIPPLE', 0),
                ('GROUPOVERRIDE', 0, 0, 0),
                ('AUTOXFADE', 1),
                [('RECORD_CFG', Symbol('Y2FsZhAAAAAIAAAA'))],
                [('RECORD_CFG',)]]
    assert loads(src) == expected


def test_dumps():
    src = [('ENTRY', 1, 2, 3), [('SUBFOLDER', '')]]
    expected = '<ENTRY 1 2 3\n  <SUBFOLDER ""\n  >\n>'
    assert dumps(src) == expected
