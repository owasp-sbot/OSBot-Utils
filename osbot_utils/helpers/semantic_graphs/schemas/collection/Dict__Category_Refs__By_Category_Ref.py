# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Category_Refs__By_Category_Ref - Maps category refs to parent category refs
# Used by Schema__Projected__Taxonomy for category_parents mapping
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref            import Category_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict


class Dict__Category_Refs__By_Category_Ref(Type_Safe__Dict):                         # Maps category refs to parent refs
    expected_key_type   = Category_Ref
    expected_value_type = Category_Ref                                               # Parent ref (empty = root)
