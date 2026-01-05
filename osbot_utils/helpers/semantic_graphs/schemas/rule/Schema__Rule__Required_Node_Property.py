# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Rule__Required_Node_Property - Rule requiring a property on nodes
#
# Specifies that nodes of a given type MUST have a specific property.
# Example: "method nodes MUST have line_number property"
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id            import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id        import Property_Name_Id
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe


class Schema__Rule__Required_Node_Property(Type_Safe):                               # Required property rule for nodes
    node_type_id     : Node_Type_Id                                                  # Which node type this applies to
    property_name_id : Property_Name_Id                                              # Which property is required
    required         : bool                    = True
