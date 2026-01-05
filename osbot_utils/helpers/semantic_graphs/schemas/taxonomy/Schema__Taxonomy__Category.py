# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Taxonomy__Category - Category in taxonomy hierarchy (pure data)
#
# Updated for Brief 3.8:
#   - Uses IDs for all cross-references (parent_id, child_ids)
#   - category_id is the instance identifier
#   - category_ref is the human-readable label (display name derivable from this)
#   - Removed 'name' and 'description' (derivable from category_ref)
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Ids     import List__Category_Ids
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id            import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref           import Category_Ref
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe


class Schema__Taxonomy__Category(Type_Safe):                                        # Category in hierarchy
    category_id  : Category_Id                                                      # Unique instance identifier
    category_ref : Category_Ref                                                     # Human-readable label (e.g., "callable")
    parent_id    : Category_Id      = None                                          # FK to parent (None = root)
    child_ids    : List__Category_Ids                                               # FKs to children
