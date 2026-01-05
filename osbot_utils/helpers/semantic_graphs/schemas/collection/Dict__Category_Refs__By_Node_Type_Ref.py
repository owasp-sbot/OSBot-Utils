# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Category_Refs__By_Node_Type_Ref - Maps node type refs to category refs
# Used by Schema__Projected__Taxonomy for node_type_categories mapping
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref            import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref           import Node_Type_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict


class Dict__Category_Refs__By_Node_Type_Ref(Type_Safe__Dict):                        # Maps node type refs to category refs
    expected_key_type   = Node_Type_Ref
    expected_value_type = Category_Ref                                               # Can be empty if no category
