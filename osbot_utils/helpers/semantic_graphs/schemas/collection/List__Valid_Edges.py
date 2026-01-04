# ═══════════════════════════════════════════════════════════════════════════════
# List__Valid_Edges - Typed collection for lists of valid edge combinations
# Used by Ontology__Utils for edge enumeration
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Valid_Edge         import Schema__Valid_Edge
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Valid_Edges(Type_Safe__List):                                            # List of valid edge combinations
    expected_type = Schema__Valid_Edge
