# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Category_Ids__By_Ref - Maps category refs to their IDs
# Used by Schema__Projected__References for correlation lookups
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id             import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref            import Category_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict


class Dict__Category_Ids__By_Ref(Type_Safe__Dict):                                   # Maps refs to IDs for categories
    expected_key_type   = Category_Ref
    expected_value_type = Category_Id
