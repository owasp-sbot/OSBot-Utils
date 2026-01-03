from typing                                                                          import Dict, List, Optional
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id              import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id              import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category import Schema__Taxonomy__Category
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text         import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version      import Safe_Str__Version


class Schema__Taxonomy(Type_Safe):                                                   # Complete taxonomy definition
    taxonomy_id   : Taxonomy_Id                                                      # Unique identifier
    version       : Safe_Str__Version            = Safe_Str__Version('1.0.0')        # Semantic version
    description   : Safe_Str__Text                                                   # What this taxonomy classifies
    root_category : Category_Id                                                      # Top-level category
    categories    : Dict[Category_Id, Schema__Taxonomy__Category]                    # id → category

    def get_category(self,
                     category_id: Category_Id
                ) -> Schema__Taxonomy__Category: # Get category by ID
        return self.categories.get(category_id)

    def get_root(self) -> Schema__Taxonomy__Category:                      # Get root category
        return self.categories.get(self.root_category)

    def get_children(self, category_id: Category_Id) -> List[Schema__Taxonomy__Category]:    # Get child categories
        category = self.categories.get(category_id)
        if not category:
            return []
        return [self.categories[c] for c in category.child_refs if c in self.categories]

    def get_parent(self, category_id: Category_Id) -> Optional[Schema__Taxonomy__Category]:  # Get parent category
        category = self.categories.get(category_id)
        if not category or not category.parent_ref:
            return None
        return self.categories.get(category.parent_ref)

    def get_ancestors(self, category_id: Category_Id) -> List[Schema__Taxonomy__Category]:   # Get all ancestors (to root)
        ancestors = []
        current = self.get_parent(category_id)
        while current:
            ancestors.append(current)
            current = self.get_parent(current.category_id)
        return ancestors

    def get_descendants(self, category_id: Category_Id) -> List[Schema__Taxonomy__Category]: # Get all descendants
        descendants = []
        children = self.get_children(category_id)
        for child in children:
            descendants.append(child)
            descendants.extend(self.get_descendants(child.category_id))
        return descendants

    def category_ids(self) -> List[Category_Id]:                                             # Get all category IDs
        return list(self.categories.keys())
