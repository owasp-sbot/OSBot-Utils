# ═══════════════════════════════════════════════════════════════════════════════
# List__Semantic_Graph__Edges - Typed collection for graph edges
# Used by Schema__Semantic_Graph for edge storage
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge import Schema__Semantic_Graph__Edge
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List               import Type_Safe__List


class List__Semantic_Graph__Edges(Type_Safe__List):                                  # List of graph edges
    expected_type = Schema__Semantic_Graph__Edge
