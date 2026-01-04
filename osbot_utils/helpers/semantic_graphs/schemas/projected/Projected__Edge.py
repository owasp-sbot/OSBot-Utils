# ═══════════════════════════════════════════════════════════════════════════════
# Projected__Edge - Human-readable edge representation
#
# Contains NO IDs - only refs and names for human consumption.
#
# Fields:
#   - from_name: The source node's name (matches a node.name)
#   - to_name:   The target node's name (matches a node.name)
#   - ref:       The relationship type (looks up in references.edges)
#
# Example: {"from_name": "method_a", "to_name": "helper_func", "ref": "calls"}
# Read as: "method_a calls helper_func"
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref            import Predicate_Ref
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id      import Safe_Str__Id


class Projected__Edge(Type_Safe):                                                    # Human-readable edge
    from_name : Safe_Str__Id                                                         # Source node name
    to_name   : Safe_Str__Id                                                         # Target node name
    ref       : Predicate_Ref                                                        # Predicate reference ("calls", "contains")
