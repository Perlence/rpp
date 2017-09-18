def findall(l, name):
    """Find all elements that start with given name.

    :returns: generator of tuples with first element as list of tree
    indexes and the second as the found value.
    """
    for i, x in enumerate(l):
        if isinstance(x, list):
            for js, y in findall(x, name):
                yield (i,) + js, y
        elif x[0] == name:
            yield (i,), x


def find(l, name):
    """Find first element that starts with given name."""
    return next(findall(l, name), None)


def update(l, indexes, value):
    """Traverse the list using given indexes and change the value.

    :param indexes: list of indexes
    :param value: new value
    """
    lastindex = indexes[-1]
    initindices = indexes[:-1]
    level = l
    for i in initindices:
        level = level[i]
    level[lastindex] = value
