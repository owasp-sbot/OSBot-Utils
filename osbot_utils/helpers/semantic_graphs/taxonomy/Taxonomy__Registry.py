# ═══════════════════════════════════════════════════════════════════════════════
# Taxonomy__Registry - Load and cache taxonomies from JSON
# Refactored to use osbot-utils file methods and proper typed collections
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Taxonomies__By_Id  import Dict__Taxonomies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id              import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id              import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy           import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category import Schema__Taxonomy__Category
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path    import Safe_Str__File__Path
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                       import type_safe
from osbot_utils.utils.Files                                                         import file_exists, file_contents
from osbot_utils.utils.Json                                                          import json_parse


class Taxonomy__Registry(Type_Safe):                                                 # Load and cache taxonomies from JSON
    cache : Dict__Taxonomies__By_Id                                                  # Cached taxonomies by ID

    @type_safe
    def load_from_file(self, file_path: Safe_Str__File__Path) -> Schema__Taxonomy:   # Load taxonomy from JSON file
        if file_exists(file_path) is False:
            return None
        raw_json = file_contents(file_path)
        if raw_json is None:
            return None
        data = json_parse(raw_json)
        if data is None:
            return None
        return self.load_from_dict(data)

    @type_safe
    def load_from_dict(self, data: dict) -> Schema__Taxonomy:                        # Load taxonomy from dictionary
        taxonomy = self.parse_taxonomy(data)
        self.cache[taxonomy.taxonomy_id] = taxonomy
        return taxonomy

    @type_safe
    def parse_taxonomy(self, data: dict) -> Schema__Taxonomy:                        # Parse taxonomy from dict
        categories = {}

        for cat_id, cat_data in data.get('categories', {}).items():
            child_refs = [Category_Id(c) for c in cat_data.get('child_refs', [])]
            category = Schema__Taxonomy__Category(category_id = Category_Id(cat_data.get('category_id', cat_id)),
                                                  name        = cat_data.get('name', cat_id)                    ,
                                                  description = cat_data.get('description', '')                 ,
                                                  parent_ref  = Category_Id(cat_data.get('parent_ref', ''))     ,
                                                  child_refs  = child_refs                                      )
            categories[cat_id] = category

        return Schema__Taxonomy(taxonomy_id   = Taxonomy_Id(data.get('taxonomy_id', '')),
                                version       = data.get('version', '1.0.0')           ,
                                description   = data.get('description', '')            ,
                                root_category = Category_Id(data.get('root_category', '')),
                                categories    = categories                             )

    @type_safe
    def get(self, taxonomy_id: Taxonomy_Id) -> Schema__Taxonomy:                     # Get cached taxonomy by ID
        return self.cache.get(taxonomy_id)

    @type_safe
    def register(self, taxonomy: Schema__Taxonomy) -> None:                          # Manually register a taxonomy
        self.cache[taxonomy.taxonomy_id] = taxonomy

    def clear(self) -> 'Taxonomy__Registry':                                         # Clear the cache
        self.cache.clear()
        return self

    def list_taxonomies(self) -> list:                                               # List all cached taxonomy IDs
        return list(self.cache.keys())
