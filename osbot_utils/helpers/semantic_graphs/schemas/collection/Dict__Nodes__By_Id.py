# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Nodes__By_Id - Typed collection mapping Node IDs to graph nodes
# Used by Schema__Semantic_Graph for node storage
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node import Schema__Semantic_Graph__Node
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                   import Node_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict


class Dict__Nodes__By_Id(Type_Safe__Dict):                                           # Maps node IDs to node objects
    expected_key_type   = Node_Id
    expected_value_type = Schema__Semantic_Graph__Node
