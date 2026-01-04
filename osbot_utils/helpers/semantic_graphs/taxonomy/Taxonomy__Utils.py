# ═══════════════════════════════════════════════════════════════════════════════
# Taxonomy__Utils - Utility operations for taxonomy navigation
# Extracted from Schema__Taxonomy to keep schemas as pure data containers
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Category_Ids          import List__Category_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Taxonomy__Categories  import List__Taxonomy__Categories
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                 import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy              import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category    import Schema__Taxonomy__Category
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                          import type_safe


class Taxonomy__Utils(Type_Safe):                                                    # Utility operations for taxonomies

    # ═══════════════════════════════════════════════════════════════════════════════
    # Category Lookup
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_category(self, taxonomy   : Schema__Taxonomy,
                           category_id: Category_Id     ) -> Schema__Taxonomy__Category:
        return taxonomy.categories.get(category_id)                                  # Get category by ID

    @type_safe
    def get_root(self, taxonomy: Schema__Taxonomy) -> Schema__Taxonomy__Category:    # Get root category
        return taxonomy.categories.get(taxonomy.root_category)

    @type_safe
    def category_ids(self, taxonomy: Schema__Taxonomy) -> List__Category_Ids:        # Get all category IDs
        result = List__Category_Ids()
        for cat_id in taxonomy.categories.keys():
            result.append(Category_Id(cat_id))
        return result

    # ═══════════════════════════════════════════════════════════════════════════════
    # Hierarchy Navigation
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_children(self, taxonomy   : Schema__Taxonomy,
                           category_id: Category_Id     ) -> List__Taxonomy__Categories:
        result   = List__Taxonomy__Categories()                                      # Get child categories
        category = taxonomy.categories.get(category_id)
        if not category:
            return result
        for child_ref in category.child_refs:
            if child_ref in taxonomy.categories:
                result.append(taxonomy.categories[child_ref])
        return result

    @type_safe
    def get_parent(self, taxonomy   : Schema__Taxonomy,
                         category_id: Category_Id     ) -> Schema__Taxonomy__Category:
        category = taxonomy.categories.get(category_id)                              # Get parent category
        if not category or not category.parent_ref:
            return None
        return taxonomy.categories.get(category.parent_ref)

    @type_safe
    def get_ancestors(self, taxonomy   : Schema__Taxonomy,
                            category_id: Category_Id     ) -> List__Taxonomy__Categories:
        ancestors = List__Taxonomy__Categories()                                     # Get all ancestors to root
        current   = self.get_parent(taxonomy, category_id)
        while current:
            ancestors.append(current)
            current = self.get_parent(taxonomy, current.category_id)
        return ancestors

    @type_safe
    def get_descendants(self, taxonomy   : Schema__Taxonomy,
                              category_id: Category_Id     ) -> List__Taxonomy__Categories:
        descendants = List__Taxonomy__Categories()                                   # Get all descendants recursively
        children    = self.get_children(taxonomy, category_id)
        for child in children:
            descendants.append(child)
            descendants.extend(self.get_descendants(taxonomy, child.category_id))
        return descendants
