# ═══════════════════════════════════════════════════════════════════════════════
# Safe_Str__Markdown - Markdown document content
# ═══════════════════════════════════════════════════════════════════════════════

import re
from osbot_utils.type_safe.primitives.core.Safe_Str                                                       import Safe_Str


class Safe_Str__Markdown(Safe_Str):                                              # Markdown content
    max_length = 1_000_000                                                       # Up to 1MB of text
    regex      = re.compile(r'[^\x20-\x7E\n\t\r]')                               # Remove non-printable ASCII
                                                                                 # Allows: space-tilde (32-126) + newline + tab + CR