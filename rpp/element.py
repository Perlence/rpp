import xml.etree.ElementPath

import attr


@attr.s
class Element:
    tag = attr.ib()
    attrib = attr.ib(default=())
    children = attr.ib(default=attr.Factory(list))

    def append(self, element):
        self.children.append(element)

    def extend(self, elements):
        self.children.extend(elements)

    def insert(self, index, element):
        self.children.insert(index, element)

    def remove(self, element):
        self.children.remove(element)

    def findall(self, path):
        return list(self.iterfind(path))

    def find(self, path):
        return next(self.iterfind(path), None)

    def iterfind(self, path):
        queryable_element = QueryableElement(self)
        found = xml.etree.ElementPath.iterfind(queryable_element, path)
        for item in found:
            if isinstance(item, ListBackedElement):
                yield item.list
            elif isinstance(item, QueryableElement):
                yield item.element

    def iter(self, tag=None):
        return iterate_element(self, tag)

    def __iter__(self):
        return iter(self.children)

    def __getitem__(self, index):
        return self.children[index]

    def __setitem__(self, index, element):
        self.children[index] = element

    def __len__(self):
        return len(self.children)


@attr.s
class QueryableElement:
    element = attr.ib()

    @property
    def tag(self):
        return self.element.tag

    def iter(self, tag=None):
        return iterate_element(self, tag)

    def __iter__(self):
        for item in self.element:
            if isinstance(item, Element):
                yield QueryableElement(item)
            elif isinstance(item, list):
                yield ListBackedElement(item)


@attr.s
class ListBackedElement:
    list = attr.ib()

    @property
    def tag(self):
        return self.list[0]

    def iter(self, tag=None):
        if tag is None or self.tag == tag:
            yield self

    def __iter__(self):
        return iter(())


def iterate_element(element, tag):
    if tag is None or element.tag == tag:
        yield element
    for item in element:
        if hasattr(item, 'iter'):
            yield from item.iter(tag)
        elif tag is None:
            yield item
