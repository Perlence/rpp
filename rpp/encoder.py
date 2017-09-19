from decimal import Decimal
from uuid import UUID

from .decoder import Element


def encode(element, indent=2, level=0):
    result = ' ' * level * indent
    if isinstance(element, str):
        result += element + '\n'
    elif isinstance(element, tuple):
        result += encode_tuple(element) + '\n'
    elif isinstance(element, Element):
        if element.items is None:
            result += encode_name_and_tuple(element)
        else:
            result += '<'
            result += encode_name_and_tuple(element)
            for item in element.items:
                result += encode(item, level=level+1)
            result += ' ' * level * indent + '>\n'
    return result


def encode_name_and_tuple(element):
    result = element.name
    if element.tuple:
        result += ' ' + encode_tuple(element.tuple)
    result += '\n'
    return result


def encode_tuple(tup):
    return ' '.join(map(tostr, tup))


def tostr(value):
    if isinstance(value, str):
        return escape_str(value)
    elif isinstance(value, Decimal):
        return format(value, 'f')
    elif isinstance(value, UUID):
        return '{{{}}}'.format(str(value).upper())
    elif value is None:
        return '-'
    else:
        return str(value)


def escape_str(value):
    if not value:
        return '""'

    should_escape = (' ', '\t', '"', "'", '`')
    if all(ch not in should_escape for ch in value):
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
