# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Taxonomy__Category - Category in taxonomy hierarchy (pure data)
#
# Categories are identified by their reference name within a taxonomy.
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Refs     import List__Category_Refs
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref            import Category_Ref
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id     import Safe_Str__Id


class Schema__Taxonomy__Category(Type_Safe):                                         # Category in hierarchy
    category_ref : Category_Ref                                                      # Reference name within taxonomy
    name         : Safe_Str__Id                                                      # Display name
    description  : Safe_Str__Text                                                    # What this category represents
    parent_ref   : Category_Ref                                                      # Parent category ref (empty if root)
    child_refs   : List__Category_Refs                                               # Child category refs
