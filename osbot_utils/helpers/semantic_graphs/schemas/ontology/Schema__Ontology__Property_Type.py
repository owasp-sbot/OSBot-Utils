# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Ontology__Property_Type - Defines a property value type
#
# Property types define how property values should be interpreted/validated.
# Examples: "integer", "boolean", "string", "float"
#
# Fields:
#   - property_type_id + property_type_id_source: Instance identity with provenance
#   - property_type_ref: Human-readable label (defined once here)
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Id         import Property_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Ref        import Property_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source       import Schema__Id__Source
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe


class Schema__Ontology__Property_Type(Type_Safe):                                    # Property type definition
    property_type_id        : Property_Type_Id                                       # Unique instance identifier
    property_type_id_source : Schema__Id__Source = None                              # ID provenance (optional sidecar)
    property_type_ref       : Property_Type_Ref                                      # Human-readable label ("integer", "boolean")
