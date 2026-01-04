# ═══════════════════════════════════════════════════════════════════════════════
# Safe_Str__Id__Seed - Seed string for deterministic ID generation
# Used with Obj_Id.from_seed() to create reproducible IDs from URIs or qualified names
# ═══════════════════════════════════════════════════════════════════════════════

import re
from osbot_utils.type_safe.primitives.core.Safe_Str                                  import Safe_Str

SAFE_STR__ID__SEED__REGEX      = re.compile(r'[^a-zA-Z0-9_:/.#\-@]')                 # Allow URI characters
SAFE_STR__ID__SEED__MAX_LENGTH = 2048                                                # URIs can be long


class Safe_Str__Id__Seed(Safe_Str):                                                  # Seed for deterministic ID generation
    regex           = SAFE_STR__ID__SEED__REGEX                                      # URI-compatible characters
    max_length      = SAFE_STR__ID__SEED__MAX_LENGTH                                 # Max 2048 characters
    allow_empty     = True                                                           # Empty allowed (for RANDOM/SEQUENTIAL sources)
    trim_whitespace = True                                                           # Clean up input