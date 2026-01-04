# ═══════════════════════════════════════════════════════════════════════════════
# Projected__Node - Human-readable node representation
#
# Contains NO IDs - only refs and names for human consumption.
#
# Fields:
#   - ref:  The type/category (looks up in references.nodes)
#   - name: The instance identity
#
# Example: {"ref": "class", "name": "MyClass"}
# Read as: "A class named MyClass"
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref            import Node_Type_Ref
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id      import Safe_Str__Id


class Projected__Node(Type_Safe):                                                    # Human-readable node
    ref  : Node_Type_Ref                                                             # Node type reference ("class", "method")
    name : Safe_Str__Id                                                              # Instance name ("MyClass")
