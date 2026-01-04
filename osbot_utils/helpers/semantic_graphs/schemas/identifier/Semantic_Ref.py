# ═══════════════════════════════════════════════════════════════════════════════
# Semantic_Ref - Base reference type for semantic graph domain objects
# Parent class for Ontology_Ref, Taxonomy_Ref, Category_Ref, Node_Type_Ref, Rule_Set_Ref
#
# IMPORTANT: This is for REFERENCES (human-readable labels from config/JSON)
#            NOT for instance IDs (use Node_Id, Edge_Id, Graph_Id, Ontology_Id, etc.)
# ═══════════════════════════════════════════════════════════════════════════════

import re
from osbot_utils.type_safe.primitives.core.Safe_Str                                  import Safe_Str

SAFE_STR__SEMANTIC_REF__REGEX      = re.compile(r'[^a-zA-Z0-9_:\-.]')                # Allow: alphanumeric, underscore, colon (CURIE), hyphen, dot
SAFE_STR__SEMANTIC_REF__MAX_LENGTH = 128


class Semantic_Ref(Safe_Str):                                                        # Base reference for semantic objects
    regex           = SAFE_STR__SEMANTIC_REF__REGEX                                  # Alphanumeric, underscore, colon, hyphen, dot
    max_length      = SAFE_STR__SEMANTIC_REF__MAX_LENGTH                             # Max 128 characters
    allow_empty     = True                                                           # Allow empty for optional refs
    trim_whitespace = True                                                           # Clean up input
