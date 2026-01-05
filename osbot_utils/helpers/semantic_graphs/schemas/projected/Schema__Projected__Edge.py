# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Projected__Edge - Human-readable edge representation
#
# Updated for Brief 3.8:
#   - Added properties: Dict of property values (Property_Name_Ref → Safe_Str__Text)
#
# Contains NO IDs - only refs and names for human consumption.
#
# Fields:
#   - from_name: The source node's name (matches a node.name)
#   - to_name:   The target node's name (matches a node.name)
#   - ref:       The relationship type (looks up in references.predicates)
#   - properties: Key-value data using refs (not IDs)
#
# Example: {"from_name": "method_a", "to_name": "helper_func", "ref": "calls", "properties": {"call_count": "3"}}
# Read as: "method_a calls helper_func 3 times"
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Projected_Properties import Dict__Projected_Properties
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref              import Predicate_Ref
from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id        import Safe_Str__Id


class Schema__Projected__Edge(Type_Safe):                                            # Human-readable edge
    from_name  : Safe_Str__Id                                                        # Source node name
    to_name    : Safe_Str__Id                                                        # Target node name
    ref        : Predicate_Ref                                                       # Predicate reference ("calls", "contains")
    properties : Dict__Projected_Properties = None                                   # Property_Name_Ref → value
