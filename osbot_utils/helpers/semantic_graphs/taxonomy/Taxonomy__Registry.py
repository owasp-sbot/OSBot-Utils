import json
from typing import Dict, Optional, List
from pathlib                                                                            import Path
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Id                 import Category_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                 import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy              import Schema__Taxonomy
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category    import Schema__Taxonomy__Category
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path       import Safe_Str__File__Path


# todo: fix cache type
class Taxonomy__Registry(Type_Safe):                                                 # Load and cache taxonomies from JSON
    cache : Dict[Taxonomy_Id, Schema__Taxonomy]                                              # Cached taxonomies by ID

    # todo: use osbot-util file methods
    def load_from_file(self, file_path: Safe_Str__File__Path) -> Schema__Taxonomy:                    # Load taxonomy from JSON file
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Taxonomy file not found: {file_path}")

        with open(path, 'r') as f:
            data = json.load(f)

        taxonomy = self.parse_taxonomy(data)
        self.cache[taxonomy.taxonomy_id] = taxonomy
        return taxonomy

    def load_from_dict(self, data: dict) -> Schema__Taxonomy:                        # Load taxonomy from dictionary
        taxonomy = self.parse_taxonomy(data)
        self.cache[taxonomy.taxonomy_id] = taxonomy
        return taxonomy

    def parse_taxonomy(self, data: dict) -> Schema__Taxonomy:                        # Parse taxonomy from dict
        categories = {}

        for cat_id, cat_data in data.get('categories', {}).items():
            child_refs = [Category_Id(c) for c in cat_data.get('child_refs', [])]
            category = Schema__Taxonomy__Category(category_id = Category_Id(cat_data.get('category_id', cat_id)) ,
                                                  name        = cat_data.get('name', cat_id)                     ,
                                                  description = cat_data.get('description', '')                  ,
                                                  parent_ref  = Category_Id(cat_data.get('parent_ref', ''))      ,
                                                  child_refs  = child_refs                                       )
            categories[cat_id] = category

        return Schema__Taxonomy(
            taxonomy_id   = Taxonomy_Id(data.get('taxonomy_id', ''))                  ,
            version       = data.get('version', '1.0.0')                             ,
            description   = data.get('description', '')                              ,
            root_category = Category_Id(data.get('root_category', ''))               ,
            categories    = categories                                               ,
        )

    def get(self, taxonomy_id: Taxonomy_Id) -> Optional[Schema__Taxonomy]:                   # Get cached taxonomy by ID
        return self.cache.get(taxonomy_id)

    def register(self, taxonomy: Schema__Taxonomy):                                  # Manually register a taxonomy
        self.cache[taxonomy.taxonomy_id] = taxonomy

    def clear(self):                                                                 # Clear the cache
        self.cache.clear()
        return self

    def list_taxonomies(self) -> List[Taxonomy_Id]:                                  # List all cached taxonomy IDs
        return list(self.cache.keys())
