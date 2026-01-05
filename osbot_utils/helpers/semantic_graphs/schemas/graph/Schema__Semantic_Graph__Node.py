# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Semantic_Graph__Node - Instance node in semantic graph
#
# Fields:
#   - node_id + node_id_source: Instance identity with provenance
#   - node_type_id: Foreign key to node type definition in ontology
#   - name: Human-readable instance name
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source       import Schema__Id__Source
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id      import Safe_Str__Id


class Schema__Semantic_Graph__Node(Type_Safe):                                       # Instance node in semantic graph
    node_id        : Node_Id                                                         # Unique instance identifier
    node_id_source : Schema__Id__Source = None                                       # ID provenance (optional sidecar)
    node_type_id   : Node_Type_Id                                                    # Foreign key to ontology node type
    name           : Safe_Str__Id                                                    # Instance name (e.g., "MyClass")
