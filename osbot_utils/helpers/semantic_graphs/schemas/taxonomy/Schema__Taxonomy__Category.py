# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Taxonomy__Category - Category in taxonomy hierarchy (pure data)
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Ids      import List__Category_Ids
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id             import Category_Id
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id     import Safe_Str__Id


class Schema__Taxonomy__Category(Type_Safe):                                         # Category in hierarchy
    category_id : Category_Id                                                        # Unique identifier
    name        : Safe_Str__Id                                                       # Category name
    description : Safe_Str__Text                                                     # What this category represents
    parent_ref  : Category_Id                                                        # Parent (empty if root)
    child_refs  : List__Category_Ids                                                 # Child categories
