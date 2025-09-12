import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


class Safe_Str__Code__Snippet(Safe_Str):     # Allows various characters needed for code snippets.
    regex = re.compile(r'[^a-zA-Z0-9_\-.\s(),;:=+\[\]{}\'"]<>')
    max_length = 1024
    trim_whitespace = False  # Preserve leading whitespace for code indentation
