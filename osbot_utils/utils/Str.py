import re
import textwrap
from html                       import escape, unescape
from osbot_utils.utils.Files    import safe_file_name

# todo: refactor this this class all str related methods (mainly from the Misc class)

ANSI_ESCAPE_PATTERN = re.compile(r'\x1b\[[0-9;]*m')

def ansi_text_visible_length(ansi_text):
    if type(ansi_text) is str:
        ansi_escape = re.compile(ANSI_ESCAPE_PATTERN)           # This regex matches the escape sequences used for text formatting
        visible_text = ansi_escape.sub('', ansi_text)       # Remove the escape sequences
        return len(visible_text)                                # Return the length of the remaining text

def ansi_to_text(ansi_text: str):
    if type(ansi_text) is str:
        return ANSI_ESCAPE_PATTERN.sub('', ansi_text)

def ansis_to_texts(ansis_texts: list):                          # todo: find a better name for this method :)
    if type(ansis_texts) is list:
        return [ansi_to_text(ansi_text) for ansi_text in ansis_texts]
    return []

def html_escape(value: str):
    return escape(value)

def html_unescape(value: str):
    return unescape(value)

def strip_quotes(value: str):                           # Remove surrounding quotes (single or double)
    if (value.startswith("'") and value.endswith("'")) or (value.startswith('"') and value.endswith('"')):
        return value[1:-1]
    return value

def str_dedent(value, strip=True):
    result = textwrap.dedent(value)
    if strip:
        result = result.strip()
    return result

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

def str_cap_snake_case(snake_str):
    """
    Converts a snake_case string to Capitalized_Snake_Case.

    Args:
        snake_str (str): The snake_case string to be converted.

    Returns:
        str: The converted string in Capitalized_Snake_Case.
    """
    return "_".join(word.capitalize() for word in snake_str.split("_"))


def trim(target):
    if type(target) is str:
        return target.strip()
    return ""

html_encode = html_escape
html_decode = html_unescape
safe_str    = str_safe