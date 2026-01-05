# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Rule__Required_Edge_Property - Rule requiring a property on edges
#
# Specifies that edges with a given predicate MUST have a specific property.
# Example: "calls edges MUST have call_count property"
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id            import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id        import Property_Name_Id
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


class Schema__Rule__Required_Edge_Property(Type_Safe):                               # Required property rule for edges
    predicate_id     : Predicate_Id                                                  # Which predicate this applies to
    property_name_id : Property_Name_Id                                              # Which property is required
    required         : bool                    = True
