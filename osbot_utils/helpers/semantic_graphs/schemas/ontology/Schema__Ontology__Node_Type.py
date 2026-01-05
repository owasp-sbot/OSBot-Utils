# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Ontology__Node_Type - Defines a node type in the ontology
#
# Updated for Brief 3.8:
#   - Added category_id: FK to taxonomy category
#
# Fields:
#   - node_type_id + node_type_id_source: Instance identity with provenance
#   - node_type_ref: Human-readable label (defined once here)
#   - category_id: Links to taxonomy category for classification
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id             import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id            import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref           import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source      import Schema__Id__Source
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


class Schema__Ontology__Node_Type(Type_Safe):                                        # Node type definition in ontology
    node_type_id        : Node_Type_Id                                               # Unique instance identifier
    node_type_id_source : Schema__Id__Source = None                                  # ID provenance (optional sidecar)
    node_type_ref       : Node_Type_Ref                                              # Human-readable label ("class", "method")
    category_id         : Category_Id        = None                                  # FK to taxonomy category
