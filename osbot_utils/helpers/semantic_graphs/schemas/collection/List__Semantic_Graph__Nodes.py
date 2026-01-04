# ═══════════════════════════════════════════════════════════════════════════════
# List__Semantic_Graph__Nodes - Typed collection for lists of graph nodes
# Used by Semantic_Graph__Utils for node queries
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node  import Schema__Semantic_Graph__Node
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Semantic_Graph__Nodes(Type_Safe__List):                                  # List of graph nodes
    expected_type = Schema__Semantic_Graph__Node
