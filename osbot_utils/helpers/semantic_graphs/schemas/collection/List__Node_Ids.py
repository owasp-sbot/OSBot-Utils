# ═══════════════════════════════════════════════════════════════════════════════
# List__Node_Ids - Typed collection for lists of node identifiers
# Used by Semantic_Graph__Utils for neighbor queries
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Node_Ids(Type_Safe__List):                                               # List of node identifiers
    expected_type = Node_Id
