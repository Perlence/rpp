import attr


@attr.s
class Element:
    name = attr.ib()
    attrs = attr.ib(default=())
    items = attr.ib(default=None)

    def findall(self, name):
        """Find all elements recursively that have given name."""
        for item in self.items:
            if not isinstance(item, Element):
                continue
            if item.name == name:
                yield item
            for subitem in item.findall(name):
                yield subitem

    def find(self, name):
        """Find first element recursively that have given name."""
        return next(self.findall(name), None)
