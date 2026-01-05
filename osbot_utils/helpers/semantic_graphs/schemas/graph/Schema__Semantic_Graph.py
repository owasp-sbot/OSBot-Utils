# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Semantic_Graph - Complete semantic graph instance (pure data)
#
# All cross-references use IDs for referential integrity:
#   - ontology_id: Foreign key to ontology definition
#   - rule_set_id: Foreign key to rule set (optional)
#
# Fields:
#   - graph_id + graph_id_source: Instance identity with provenance
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id          import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                 import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                 import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source          import Schema__Id__Source
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                      import Graph_Id


class Schema__Semantic_Graph(Type_Safe):                                             # Complete semantic graph instance
    graph_id        : Graph_Id                                                       # Unique instance identifier
    graph_id_source : Schema__Id__Source         = None                              # ID provenance (optional sidecar)
    ontology_id     : Ontology_Id                                                    # Foreign key to ontology
    rule_set_id     : Rule_Set_Id                = None                              # Foreign key to rule set (optional)
    nodes           : Dict__Nodes__By_Id                                             # Node_Id → node
    edges           : List__Semantic_Graph__Edges                                    # All edges
