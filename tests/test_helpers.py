from rpp import findall, update


def test_findall():
    l = [('NAME', 1, 2), [('NUN', 1, 5.234, 'x')], [('SUS', 3)]]
    assert list(findall(l, 'SUS')) == [((2, 0), ('SUS', 3))]


def test_update():
    l = [('NAME', 1, 2), [('NUN', 1, 5.234, 'x')], [('SUS', 3)]]
    update(l, [1, 0], ('LUL', 42))
    assert l == [('NAME', 1, 2), [('LUL', 42)], [('SUS', 3)]]
