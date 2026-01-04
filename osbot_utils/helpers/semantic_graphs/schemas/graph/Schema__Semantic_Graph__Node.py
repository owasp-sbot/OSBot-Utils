# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Semantic_Graph__Node - Instance node in semantic graph
#
# Fields:
#   - node_id + node_id_source: Instance identity with provenance
#   - node_type: Reference to node type definition in ontology
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref            import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source       import Schema__Id__Source
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id      import Safe_Str__Id


class Schema__Semantic_Graph__Node(Type_Safe):                                       # Instance node in semantic graph
    node_id        : Node_Id                                                         # Unique instance identifier
    node_id_source : Schema__Id__Source          = None                              # ID provenance (optional sidecar)
    node_type      : Node_Type_Ref                                                   # Reference to ontology node type
    name           : Safe_Str__Id                                                    # Display name
    line_number    : Safe_UInt                                                       # Optional source location
