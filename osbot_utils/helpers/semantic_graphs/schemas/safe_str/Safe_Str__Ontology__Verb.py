import re
from osbot_utils.type_safe.primitives.core.Safe_Str                                  import Safe_Str


class Safe_Str__Ontology__Verb(Safe_Str):                                            # Relationship verb for edges
    max_length = 64                                                                  # e.g., "has", "inherits_from"
    regex      = re.compile(r'[^a-z_]')                                              # Lowercase with underscores only
