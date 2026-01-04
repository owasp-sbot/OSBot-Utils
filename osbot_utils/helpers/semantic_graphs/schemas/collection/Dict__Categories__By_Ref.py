# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Categories__By_Ref - Typed collection mapping category refs to categories
# Used by Schema__Taxonomy for category storage
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref             import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category import Schema__Taxonomy__Category
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class Dict__Categories__By_Ref(Type_Safe__Dict):                                     # Maps category refs to categories
    expected_key_type   = Category_Ref
    expected_value_type = Schema__Taxonomy__Category
