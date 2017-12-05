import attr

from rpp import Element


def test_findall():
    el = Element('NAME', (1, 2))
    assert el.findall('SUS') == []

    el = Element('SUS', (1, 2), [
        Element('NUN', (1, 5.234, 'x'), [
            ['BEEP', 'BOOP'],
        ]),
        ['SUS', 3],
    ])
    assert el.findall('SUS') == [el[1]]
    assert list(el.iterfind('SUS')) == [el[1]]
    assert el.find('./NUN') is el[0]
    assert el.find('./SUS') is el[1]
    assert el.find('.//BEEP') is el[0][0]

    sus = el.find('./SUS')
    sus[1] = 4
    assert el[1][1] == 4


def test_remove():
    el = Element('NAME', (1, 2), [
        Element('NUN', (1, 5.234, 'x'), []),
        ['SUS', 3],
    ])
    el.remove(el[0])
    assert el == Element('NAME', (1, 2), [
        ['SUS', 3],
    ])
    el.remove(el[0])
    assert el == Element('NAME', (1, 2), [])


def test_iter():
    el = Element('NAME', (1, 2), [
        Element('NAME', (1, 5.234, 'x'), []),
        ['NAME', 3],
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
    expected = Element('TRACK', children=[['ITEM', '0']])

    el = attr.evolve(track, children=[])
    el.append(['ITEM', '0'])
    assert el == expected

    el = attr.evolve(track, children=[])
    el.extend([['ITEM', '0']])
    assert el == expected

    el = attr.evolve(track, children=[])
    el.insert(0, ['ITEM', '0'])
    assert el == expected

    el = attr.evolve(expected, children=[['ITEM', '0']])
    el.remove(el[0])
    assert el == attr.evolve(track, children=[])
