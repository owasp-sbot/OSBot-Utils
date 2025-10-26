import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str

# todo: review this regex, since should we be allowing any non text values here?
TYPE_SAFE_STR__HTTP__USER_AGENT__REGEX      = re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]')  # Filter control chars
TYPE_SAFE_STR__HTTP__USER_AGENT__MAX_LENGTH = 512

class Safe_Str__Http__User_Agent(Safe_Str):
    """
    Safe string class for HTTP User-Agent header values.
    Allows standard user agent strings with various characters.
    Example: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    """
    regex                      = TYPE_SAFE_STR__HTTP__USER_AGENT__REGEX
    max_length                 = TYPE_SAFE_STR__HTTP__USER_AGENT__MAX_LENGTH
    trim_whitespace            = True