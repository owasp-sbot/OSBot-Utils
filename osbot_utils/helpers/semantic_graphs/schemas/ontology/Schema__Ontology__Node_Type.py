# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Ontology__Node_Type - Defines a node type in the ontology
#
# Fields:
#   - node_type_id + node_type_id_source: Instance identity with provenance
#   - node_type_ref: Human-readable label (defined once here)
#
# Note: Relationships are now handled by Schema__Ontology__Predicate and
#       Schema__Ontology__Edge_Rule at the ontology level, not per node type.
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref            import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source       import Schema__Id__Source
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text         import Safe_Str__Text


class Schema__Ontology__Node_Type(Type_Safe):                                        # Node type definition in ontology
    node_type_id        : Node_Type_Id                                               # Unique instance identifier
    node_type_id_source : Schema__Id__Source = None                                  # ID provenance (optional sidecar)
    node_type_ref       : Node_Type_Ref                                              # Human-readable label ("class", "method")
    description         : Safe_Str__Text     = None                                  # Optional description
