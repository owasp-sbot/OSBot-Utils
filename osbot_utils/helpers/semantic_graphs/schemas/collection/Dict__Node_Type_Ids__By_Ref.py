# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Node_Type_Ids__By_Ref - Maps node type refs to their IDs
# Used by Projected__References for correlation lookups
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref            import Node_Type_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class Dict__Node_Type_Ids__By_Ref(Type_Safe__Dict):                                  # Maps refs to IDs for node types
    expected_key_type   = Node_Type_Ref
    expected_value_type = Node_Type_Id
