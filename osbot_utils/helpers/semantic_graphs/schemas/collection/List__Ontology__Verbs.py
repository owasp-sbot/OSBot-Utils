# ═══════════════════════════════════════════════════════════════════════════════
# List__Ontology__Verbs - Typed collection for lists of ontology verbs
# Used by Ontology__Utils for verb queries
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Ontology__Verbs(Type_Safe__List):                                        # List of ontology verbs
    expected_type = Safe_Str__Ontology__Verb
