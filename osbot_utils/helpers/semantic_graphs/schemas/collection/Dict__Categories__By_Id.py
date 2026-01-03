# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Categories__By_Id - Typed collection mapping Category IDs to categories
# Used by Schema__Taxonomy for category storage
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id              import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category import Schema__Taxonomy__Category
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class Dict__Categories__By_Id(Type_Safe__Dict):                                      # Maps category IDs to categories
    expected_key_type   = Category_Id
    expected_value_type = Schema__Taxonomy__Category
