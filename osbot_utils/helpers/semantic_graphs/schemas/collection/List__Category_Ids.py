# ═══════════════════════════════════════════════════════════════════════════════
# List__Category_Ids - Typed collection for lists of category identifiers
# Used by Schema__Taxonomy__Category for child references
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id import Category_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List   import Type_Safe__List


class List__Category_Ids(Type_Safe__List):                                           # List of category identifiers
    expected_type = Category_Id
