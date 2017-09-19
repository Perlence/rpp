import attr

from rpp import Element


def test_findall():
    el = Element('NAME', (1, 2))
    assert el.findall('SUS') == []

    el = Element('SUS', (1, 2), [
        Element('NUN', (1, 5.234, 'x'), []),
        Element('SUS', (3,), []),
    ])
    assert el.findall('SUS') == [el[1]]
    assert list(el.iterfind('SUS')) == [el[1]]
    assert el.find('./SUS') == el[1]


def test_remove():
    el = Element('NAME', (1, 2), [
        Element('NUN', (1, 5.234, 'x'), []),
        Element('SUS', (3,), []),
    ])
    el.remove(el[0])
    assert el == Element('NAME', (1, 2), [
        Element('SUS', (3,), []),
    ])


def test_iter():
    el = Element('NAME', (1, 2), [
        Element('NAME', (1, 5.234, 'x'), []),
        Element('NAME', (3,), []),
    ])
    assert list(el.iter()) == [
        el,
        el[0],
        el[1],
    ]

    assert len(el) == 2

    el[1] = Element('NAME', (), [])
    assert el == Element('NAME', (1, 2), [
        Element('NAME', (1, 5.234, 'x'), []),
        Element('NAME', (), []),
    ])


def test_no_subelements():
    track = Element('TRACK')
    expected = Element('TRACK', children=[Element('ITEM')])
    el = attr.evolve(track)
    el.append(Element('ITEM'))
    assert el == expected

    el = attr.evolve(track)
    el.extend([Element('ITEM')])
    assert el == expected

    el = attr.evolve(track)
    el.insert(0, Element('ITEM'))
    assert el == expected

    el = attr.evolve(expected)
    el.remove(el[0])
    assert el == attr.evolve(track, children=[])
