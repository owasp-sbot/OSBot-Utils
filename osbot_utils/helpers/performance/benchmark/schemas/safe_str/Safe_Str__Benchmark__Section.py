# ═══════════════════════════════════════════════════════════════════════════════
# Safe_Str__Benchmark__Section - Section identifier primitive
# e.g., "A", "B", "Python", "Type_Safe"
# ═══════════════════════════════════════════════════════════════════════════════
import re
from osbot_utils.type_safe.primitives.core.Safe_Str import Safe_Str


class Safe_Str__Benchmark__Section(Safe_Str):                                    # Section identifier
    max_length = 50
    regex      = re.compile(r'[^a-zA-Z0-9 _]')