# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Semantic_Graph - Complete semantic graph instance (pure data)
# Business logic has been moved to Semantic_Graph__Utils
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id          import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                 import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                 import Rule_Set_Id
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version         import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                      import Graph_Id


class Schema__Semantic_Graph(Type_Safe):                                             # Complete semantic graph instance
    graph_id     : Graph_Id                                                          # Unique identifier
    version      : Safe_Str__Version = '1.0.0'                                       # Graph version
    ontology_ref : Ontology_Id                                                       # Which ontology defines types
    rule_set_ref : Rule_Set_Id                                                       # Optional rule set
    nodes        : Dict__Nodes__By_Id                                                # node_id → node
    edges        : List__Semantic_Graph__Edges                                       # All edges
