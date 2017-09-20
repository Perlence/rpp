from decimal import Decimal

from .element import Element
from .scanner import tokenize


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
        return quote_string(value)
    elif isinstance(value, Decimal):
        return format(value, 'f')
    elif value is None:
        return '-'
    else:
        return str(value)


def quote_string(value):
    if not value:
        return '""'
    if not should_quote(value):
        return value
    quote, value = quote_mark(value)
    return '{quote}{value}{quote}'.format(quote=quote, value=value)


def should_quote(s):
    return starts_with_quote(s) or has_whitespace(s) or looks_like_null_int_float(s)


def starts_with_quote(s):
    quotes = '"\'`'
    return s[0] in quotes


def has_whitespace(s):
    whitespace = ' \t'
    return any(ch in whitespace for ch in s)


def looks_like_null_int_float(s):
    (token, *etc) = tokenize(s + ' ')
    return token.type in ('NULL', 'INT', 'FLOAT')


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
