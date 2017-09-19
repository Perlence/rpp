import xml.etree.ElementPath

import attr


@attr.s
class Element:
    tag = attr.ib()
    attrib = attr.ib(default=())
    children = attr.ib(default=None)

    def has_subelements(self):
        return self.children is not None

    def append(self, element):
        self._ensure_children_list()
        self.children.append(element)

    def extend(self, elements):
        self._ensure_children_list()
        self.children.extend(elements)

    def insert(self, index, element):
        self._ensure_children_list()
        self.children.insert(index, element)

    def remove(self, element):
        self._ensure_children_list()
        self.children.remove(element)

    def findall(self, match):
        return xml.etree.ElementPath.findall(self, match)

    def find(self, match):
        return xml.etree.ElementPath.find(self, match)

    def iterfind(self, match):
        return xml.etree.ElementPath.iterfind(self, match)

    def iter(self, tag=None):
        if tag is None or self.tag == tag:
            yield self
        if not len(self):
            return
        for item in self:
            if not isinstance(item, Element):
                if tag is None:
                    yield item
                continue
            for subitem in item.iter(tag):
                yield subitem

    def __iter__(self):
        if not self.has_subelements():
            return iter(())
        return iter(self.children)

    def __getitem__(self, index):
        if not self.has_subelements():
            raise IndexError('there are no subelements')
        return self.children[index]

    def __setitem__(self, index, element):
        self._ensure_children_list()
        self.children[index] = element

    def __len__(self):
        if not self.has_subelements():
            return 0
        return len(self.children)

    def _ensure_children_list(self):
        if self.has_subelements():
            return
        self.children = []
