# ═══════════════════════════════════════════════════════════════════════════════
# Taxonomy__Utils - Operations on Schema__Taxonomy (business logic)
#
# Updated for Brief 3.8:
#   - All operations use IDs for lookups (parent_id, child_ids)
#   - get_category takes category_id
#   - Hierarchy navigation uses ID-based references
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Ids         import List__Category_Ids
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref               import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy             import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category   import Schema__Taxonomy__Category
from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                         import type_safe


class Taxonomy__Utils(Type_Safe):                                                      # Operations on taxonomy schemas

    @type_safe
    def get_category(self                      ,
                     taxonomy    : Schema__Taxonomy,
                     category_id : Category_Id     ) -> Schema__Taxonomy__Category:    # Get category by ID
        return taxonomy.categories.get(category_id)

    @type_safe
    def get_category_by_ref(self                      ,
                            taxonomy     : Schema__Taxonomy,
                            category_ref : Category_Ref    ) -> Schema__Taxonomy__Category:  # Get category by ref (linear scan)
        for category in taxonomy.categories.values():
            if category.category_ref == category_ref:
                return category
        return None

    @type_safe
    def get_category_id_by_ref(self                      ,
                               taxonomy     : Schema__Taxonomy,
                               category_ref : Category_Ref    ) -> Category_Id:        # Resolve ref → ID
        category = self.get_category_by_ref(taxonomy, category_ref)
        if category is None:
            return None
        return category.category_id

    @type_safe
    def get_category_ref_by_id(self                      ,
                               taxonomy    : Schema__Taxonomy,
                               category_id : Category_Id     ) -> Category_Ref:        # Resolve ID → ref
        category = self.get_category(taxonomy, category_id)
        if category is None:
            return None
        return category.category_ref

    @type_safe
    def has_category(self                      ,
                     taxonomy    : Schema__Taxonomy,
                     category_id : Category_Id     ) -> bool:                          # Check if category exists by ID
        return category_id in taxonomy.categories

    @type_safe
    def all_category_ids(self                  ,
                         taxonomy : Schema__Taxonomy) -> List__Category_Ids:           # All category IDs
        result = List__Category_Ids()
        for category_id in taxonomy.categories.keys():
            result.append(category_id)
        return result

    @type_safe
    def get_root_category(self                  ,
                          taxonomy : Schema__Taxonomy) -> Schema__Taxonomy__Category:  # Get root category
        return self.get_category(taxonomy, taxonomy.root_id)

    @type_safe
    def get_parent(self                        ,
                   taxonomy    : Schema__Taxonomy,
                   category_id : Category_Id     ) -> Schema__Taxonomy__Category:      # Get parent category
        category = self.get_category(taxonomy, category_id)
        if category is None or category.parent_id is None:
            return None
        return self.get_category(taxonomy, category.parent_id)

    @type_safe
    def get_children(self                      ,
                     taxonomy    : Schema__Taxonomy,
                     category_id : Category_Id     ) -> List__Category_Ids:            # Get child IDs
        category = self.get_category(taxonomy, category_id)
        if category is None:
            return List__Category_Ids()
        return category.child_ids

    @type_safe
    def get_ancestors(self                     ,
                      taxonomy    : Schema__Taxonomy,
                      category_id : Category_Id     ) -> List__Category_Ids:           # All ancestor IDs (parent → root)
        result   = List__Category_Ids()
        category = self.get_category(taxonomy, category_id)
        while category is not None and category.parent_id is not None:
            result.append(category.parent_id)
            category = self.get_category(taxonomy, category.parent_id)
        return result

    @type_safe
    def get_descendants(self                   ,
                        taxonomy    : Schema__Taxonomy,
                        category_id : Category_Id     ) -> List__Category_Ids:         # All descendant IDs (recursive)
        result   = List__Category_Ids()
        category = self.get_category(taxonomy, category_id)
        if category is None:
            return result
        for child_id in category.child_ids:
            result.append(child_id)
            descendants = self.get_descendants(taxonomy, child_id)
            for desc_id in descendants:
                result.append(desc_id)
        return result

    @type_safe
    def is_ancestor_of(self                         ,
                       taxonomy    : Schema__Taxonomy,
                       category_id : Category_Id     ,
                       child_id    : Category_Id     ) -> bool:                        # Check if category is ancestor
        ancestors = self.get_ancestors(taxonomy, child_id)
        return category_id in ancestors

    @type_safe
    def is_descendant_of(self                       ,
                         taxonomy    : Schema__Taxonomy,
                         category_id : Category_Id     ,
                         parent_id   : Category_Id     ) -> bool:                      # Check if category is descendant
        ancestors = self.get_ancestors(taxonomy, category_id)
        return parent_id in ancestors

    @type_safe
    def depth(self                             ,
              taxonomy    : Schema__Taxonomy   ,
              category_id : Category_Id        ) -> int:                               # Depth in tree (root = 0)
        ancestors = self.get_ancestors(taxonomy, category_id)
        return len(ancestors)
