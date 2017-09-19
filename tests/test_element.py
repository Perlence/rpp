from rpp import Element


def test_findall():
    el = Element('NAME', (1, 2), [
        Element('NUN', (1, 5.234, 'x'), []),
        Element('SUS', (3,), []),
    ])
    assert list(el.findall('SUS')) == [el.items[1]]


def test_update():
    el = Element('NAME', (1, 2), [
        Element('NUN', (1, 5.234, 'x'), []),
        Element('SUS', (3,), []),
    ])
    el.items[0] = Element('LUL', (42,), [])
    assert el == Element('NAME', (1, 2), [
        Element('LUL', (42,), []),
        Element('SUS', (3,), []),
    ])
