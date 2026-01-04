# ═══════════════════════════════════════════════════════════════════════════════
# Semantic_Id - Base identifier type for semantic graph domain objects
# Parent class for Ontology_Id, Taxonomy_Id, Category_Id, Node_Type_Id, Rule_Set_Id
# ═══════════════════════════════════════════════════════════════════════════════

import re
from osbot_utils.type_safe.primitives.core.Safe_Str                                  import Safe_Str

SAFE_STR__SEMANTIC_ID__REGEX      = re.compile(r'[^a-zA-Z0-9_\-.]')
SAFE_STR__SEMANTIC_ID__MAX_LENGTH = 128


class Semantic_Id(Safe_Str):                                                         # Base identifier for semantic objects
    regex           = SAFE_STR__SEMANTIC_ID__REGEX                                   # Alphanumeric, underscore, dash, dot
    max_length      = SAFE_STR__SEMANTIC_ID__MAX_LENGTH                              # Max 128 characters
    allow_empty     = True                                                           # Allow empty for optional refs
    trim_whitespace = True                                                           # Clean up input
