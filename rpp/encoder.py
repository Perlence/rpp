from decimal import Decimal

from .element import Element


def encode(element, indent=2, level=0):
    result = ' ' * level * indent
    if isinstance(element, str):
        result += element + '\n'
    elif isinstance(element, tuple):
        result += encode_tuple(element) + '\n'
    elif isinstance(element, Element):
        if not element.has_subelements():
            result += encode_tag_and_attrib(element)
        else:
            result += '<'
            result += encode_tag_and_attrib(element)
            for item in element:
                result += encode(item, level=level+1)
            result += ' ' * level * indent + '>\n'
    return result


def encode_tag_and_attrib(element):
    result = element.tag
    if element.attrib:
        result += ' ' + encode_tuple(element.attrib)
    result += '\n'
    return result


def encode_tuple(tup):
    return ' '.join(map(tostr, tup))


def tostr(value):
    if isinstance(value, str):
        return escape_str(value)
    elif isinstance(value, Decimal):
        return format(value, 'f')
    elif value is None:
        return '-'
    else:
        return str(value)


def escape_str(value):
    if not value:
        return '""'

    whitespace = ' \t'
    if not starts_with_quote(value) and all(ch not in whitespace for ch in value):
        return value

    quote = '"'
    if '"' in value:
        quote = "'"
    if "'" in value:
        quote = '`'
    if '`' in value:
        quote = '`'
        value = value.replace('`', "'")
    return '{quote}{value}{quote}'.format(quote=quote, value=value)


def starts_with_quote(s):
    quotes = '"\'`'
    return s[0] in quotes
