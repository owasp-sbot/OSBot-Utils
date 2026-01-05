# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Semantic_Graph__Edge - Instance edge in semantic graph
#
# Updated for Brief 3.8:
#   - Added properties: Dict of property values (Property_Name_Id → Safe_Str__Text)
#
# Fields:
#   - edge_id + edge_id_source: Instance identity with provenance
#   - from_node_id, to_node_id: FKs to nodes in this graph
#   - predicate_id: FK to predicate definition in ontology
#   - properties: Key-value data attached to this edge
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Edge_Properties   import Dict__Edge_Properties
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id            import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source      import Schema__Id__Source
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                   import Node_Id


class Schema__Semantic_Graph__Edge(Type_Safe):                                       # Instance edge in semantic graph
    edge_id        : Edge_Id                                                         # Unique instance identifier
    edge_id_source : Schema__Id__Source    = None                                    # ID provenance (optional sidecar)
    from_node_id   : Node_Id                                                         # Source node (FK)
    to_node_id     : Node_Id                                                         # Target node (FK)
    predicate_id   : Predicate_Id                                                    # Relationship type (FK to ontology)
    properties     : Dict__Edge_Properties = None                                    # Property_Name_Id → value
