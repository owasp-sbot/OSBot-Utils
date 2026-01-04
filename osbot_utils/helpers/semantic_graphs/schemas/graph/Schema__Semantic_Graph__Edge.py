# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Semantic_Graph__Edge - Instance edge in semantic graph
#
# Fields:
#   - edge_id + edge_id_source: Instance identity with provenance
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source       import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                    import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id


class Schema__Semantic_Graph__Edge(Type_Safe):                                       # Instance edge in semantic graph
    edge_id        : Edge_Id                                                         # Unique instance identifier
    edge_id_source : Schema__Id__Source          = None                              # ID provenance (optional sidecar)
    from_node      : Node_Id                                                         # Source node
    verb           : Safe_Str__Ontology__Verb                                        # Relationship verb
    to_node        : Node_Id                                                         # Target node
    line_number    : Safe_UInt                   = Safe_UInt(0)                      # Optional source location
