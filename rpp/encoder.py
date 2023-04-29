from collections.abc import Iterable
from decimal import Decimal

from .element import Element
from .scanner import starts_with_quote, starts_with_pipe


def encode(element, indent=2, level=0):
    result = ' ' * level * indent
    if isinstance(element, Element):
        result += '<'
        result += encode_tag_and_attrib(element)
        for item in element:
            result += encode(item, level=level+1)
        result += ' ' * level * indent + '>\n'
    elif isinstance(element, str):
        result += quote_string(element, quote_pipe=False) + '\n'
    else:
        result += encode_value(element) + '\n'
    return result


def encode_tag_and_attrib(element):
    result = element.tag
    if element.attrib:
        result += ' ' + encode_iterable(element.attrib)
    result += '\n'
    return result


def encode_value(value):
    if isinstance(value, str):
        return quote_string(value)
    elif isinstance(value, Iterable):
        return encode_iterable(value)
    elif isinstance(value, Decimal):
        return quote_string(format(value, 'f'))
    else:
        return quote_string(str(value))


def encode_iterable(iterable):
    return ' '.join(map(encode_value, iterable))


def quote_string(value, quote_pipe=True):
    if not value:
        return '""'
    if not should_quote(value, quote_pipe):
        return value
    quote, value = quote_mark(value)
    return '{quote}{value}{quote}'.format(quote=quote, value=value)


def should_quote(s, quote_pipe):
    return (quote_pipe or not starts_with_pipe(s)) and (starts_with_quote(s) or has_whitespace(s))


def has_whitespace(s):
    whitespace = ' \t'
    return any(ch in whitespace for ch in s)


def quote_mark(s):
    quote = '"'
    if '"' in s:
        quote = "'"
    if "'" in s:
        quote = '`'
    if '`' in s:
        quote = '`'
        s = s.replace('`', "'")
    return quote, s
