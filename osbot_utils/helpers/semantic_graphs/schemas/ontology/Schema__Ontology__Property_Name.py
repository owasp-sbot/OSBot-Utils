# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Ontology__Property_Name - Defines a property name in the ontology
#
# Property names are like "line_number", "is_async", "call_count".
# Each property name can optionally reference a property type for validation.
#
# Fields:
#   - property_name_id + property_name_id_source: Instance identity with provenance
#   - property_name_ref: Human-readable label (defined once here)
#   - property_type_id: FK to type (None = string, no validation)
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id        import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Ref       import Property_Name_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Id        import Property_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source      import Schema__Id__Source
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


class Schema__Ontology__Property_Name(Type_Safe):                                    # Property name definition
    property_name_id        : Property_Name_Id                                       # Unique instance identifier
    property_name_id_source : Schema__Id__Source = None                              # ID provenance (optional sidecar)
    property_name_ref       : Property_Name_Ref                                      # Human-readable label ("line_number")
    property_type_id        : Property_Type_Id   = None                              # FK to type (None = string)
