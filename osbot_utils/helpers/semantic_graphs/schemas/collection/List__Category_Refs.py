# ═══════════════════════════════════════════════════════════════════════════════
# List__Category_Refs - Typed collection for lists of category references
# Used by Schema__Taxonomy__Category for child references
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref             import Category_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Category_Refs(Type_Safe__List):                                          # List of category references
    expected_type = Category_Ref
