# ═══════════════════════════════════════════════════════════════════════════════
# Taxonomy__Utils - Operations on Schema__Taxonomy (business logic)
# All operations take taxonomy as first parameter - schemas remain pure data
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Refs         import List__Category_Refs
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy              import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category    import Schema__Taxonomy__Category
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                          import type_safe


class Taxonomy__Utils(Type_Safe):                                                       # Operations on taxonomy schemas

    @type_safe
    def get_category(self                       ,
                     taxonomy     : Schema__Taxonomy,
                     category_ref : Category_Ref    ) -> Schema__Taxonomy__Category:    # Get category by ref
        return taxonomy.categories.get(category_ref)

    @type_safe
    def has_category(self                       ,
                     taxonomy     : Schema__Taxonomy,
                     category_ref : Category_Ref    ) -> bool:                          # Check if category exists
        return category_ref in taxonomy.categories

    @type_safe
    def all_category_refs(self                  ,
                          taxonomy : Schema__Taxonomy) -> List__Category_Refs:          # All category refs
        result = List__Category_Refs()
        for ref in taxonomy.categories.keys():
            result.append(ref)
        return result

    @type_safe
    def get_root_category(self                  ,
                          taxonomy : Schema__Taxonomy) -> Schema__Taxonomy__Category:   # Get root category
        return self.get_category(taxonomy, taxonomy.root_category)

    @type_safe
    def get_parent(self                         ,
                   taxonomy     : Schema__Taxonomy,
                   category_ref : Category_Ref    ) -> Schema__Taxonomy__Category:      # Get parent category
        category = self.get_category(taxonomy, category_ref)
        if category is None or not category.parent_ref:
            return None
        return self.get_category(taxonomy, category.parent_ref)

    @type_safe
    def get_children(self                       ,
                     taxonomy     : Schema__Taxonomy,
                     category_ref : Category_Ref    ) -> List__Category_Refs:           # Get child refs
        category = self.get_category(taxonomy, category_ref)
        if category is None:
            return List__Category_Refs()
        return category.child_refs

    @type_safe
    def get_ancestors(self                      ,
                      taxonomy     : Schema__Taxonomy,
                      category_ref : Category_Ref    ) -> List__Category_Refs:          # All ancestor refs (parent → root)
        result   = List__Category_Refs()
        category = self.get_category(taxonomy, category_ref)
        while category is not None and category.parent_ref:
            result.append(category.parent_ref)
            category = self.get_category(taxonomy, category.parent_ref)
        return result

    @type_safe
    def get_descendants(self                    ,
                        taxonomy     : Schema__Taxonomy,
                        category_ref : Category_Ref    ) -> List__Category_Refs:        # All descendant refs (recursive)
        result   = List__Category_Refs()
        category = self.get_category(taxonomy, category_ref)
        if category is None:
            return result
        for child_ref in category.child_refs:
            result.append(child_ref)
            descendants = self.get_descendants(taxonomy, child_ref)
            for desc_ref in descendants:
                result.append(desc_ref)
        return result

    @type_safe
    def is_ancestor_of(self                          ,
                       taxonomy     : Schema__Taxonomy,
                       category_ref : Category_Ref    ,
                       child_ref    : Category_Ref    ) -> bool:                        # Check if category is ancestor
        ancestors = self.get_ancestors(taxonomy, child_ref)
        return category_ref in ancestors

    @type_safe
    def is_descendant_of(self                        ,
                         taxonomy     : Schema__Taxonomy,
                         category_ref : Category_Ref    ,
                         parent_ref   : Category_Ref    ) -> bool:                      # Check if category is descendant
        ancestors = self.get_ancestors(taxonomy, category_ref)
        return parent_ref in ancestors

    @type_safe
    def depth(self                              ,
              taxonomy     : Schema__Taxonomy   ,
              category_ref : Category_Ref       ) -> int:                               # Depth in tree (root = 0)
        ancestors = self.get_ancestors(taxonomy, category_ref)
        return len(ancestors)
