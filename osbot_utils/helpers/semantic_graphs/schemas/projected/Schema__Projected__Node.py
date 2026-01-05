# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Projected__Node - Human-readable node representation
#
# Updated for Brief 3.8:
#   - Added properties: Dict of property values (Property_Name_Ref → Safe_Str__Text)
#
# Contains NO IDs - only refs and names for human consumption.
#
# Fields:
#   - ref:  The type/category (looks up in references.node_types)
#   - name: The instance identity
#   - properties: Key-value data using refs (not IDs)
#
# Example: {"ref": "class", "name": "MyClass", "properties": {"line_number": "42"}}
# Read as: "A class named MyClass at line 42"
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Projected_Properties import Dict__Projected_Properties
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref              import Node_Type_Ref
from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id        import Safe_Str__Id


class Schema__Projected__Node(Type_Safe):                                            # Human-readable node
    ref        : Node_Type_Ref                                                       # Node type reference ("class", "method")
    name       : Safe_Str__Id                                                        # Instance name ("MyClass")
    properties : Dict__Projected_Properties = None                                   # Property_Name_Ref → value
