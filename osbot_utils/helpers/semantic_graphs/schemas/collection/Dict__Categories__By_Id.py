# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Categories__By_Id - Maps category IDs to category definitions
# Used by Schema__Taxonomy for category storage (Brief 3.8: ID-based)
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category   import Schema__Taxonomy__Category
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                  import Type_Safe__Dict


class Dict__Categories__By_Id(Type_Safe__Dict):                                      # Maps category IDs to definitions
    expected_key_type   = Category_Id
    expected_value_type = Schema__Taxonomy__Category
