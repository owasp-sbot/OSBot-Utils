import textwrap
from html import escape, unescape

from osbot_utils.utils.Files import safe_file_name


def html_escape(value):
    return escape(value)

def html_unescape(value):
    return unescape(value)

def str_dedent(value):
    return textwrap.dedent(value).strip()

def str_index(target:str, source:str):
    try:
        return target.index(source)
    except:
        return -1

def str_join(delimiter, values):
    return delimiter.join(values)

def str_max_width(target, value):
    return str(target)[:value]

def str_safe(value):
    return safe_file_name(value)

def str_starts_with(source, prefix):
    if source is None or prefix is None:
        return False
    else:
        return source.startswith(prefix)

def str_unicode_escape(target):
    return str(target).encode('unicode_escape').decode("utf-8")


def trim(target):
    if type(target) is str:
        return target.strip()
    return ""


html_encode = html_escape
html_decode = html_unescape