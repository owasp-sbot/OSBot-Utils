# ═══════════════════════════════════════════════════════════════════════════════
# Taxonomy__Registry - Load and cache taxonomies from JSON
# Refactored to use osbot-utils file methods and proper typed collections
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Taxonomies__By_Id  import Dict__Taxonomies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Taxonomy_Ids       import List__Taxonomy_Ids
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id              import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy           import Schema__Taxonomy
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path    import Safe_Str__File__Path
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                       import type_safe
from osbot_utils.utils.Json                                                          import json_file_load


class Taxonomy__Registry(Type_Safe):                                                 # Load and cache taxonomies from JSON
    cache : Dict__Taxonomies__By_Id                                                  # Cached taxonomies by ID

    @type_safe
    def load_from_file(self, file_path: Safe_Str__File__Path) -> Schema__Taxonomy:   # Load taxonomy from JSON file
        data = json_file_load(file_path)
        if data == {}:                                                               # If file doesn't exist or parse failed
            return None
        return self.load_from_dict(data)

    @type_safe
    def load_from_dict(self, data: dict) -> Schema__Taxonomy:                        # Load taxonomy from dictionary
        taxonomy = self.parse_taxonomy(data)
        self.cache[taxonomy.taxonomy_id] = taxonomy
        return taxonomy

    @type_safe
    def parse_taxonomy(self, data: dict) -> Schema__Taxonomy:                        # Parse taxonomy from dict
        return Schema__Taxonomy.from_json(data)

    @type_safe
    def get(self, taxonomy_id: Taxonomy_Id) -> Schema__Taxonomy:                     # Get cached taxonomy by ID
        return self.cache.get(taxonomy_id)

    @type_safe
    def register(self, taxonomy: Schema__Taxonomy) -> None:                          # Manually register a taxonomy
        self.cache[taxonomy.taxonomy_id] = taxonomy

    @type_safe
    def clear(self) -> 'Taxonomy__Registry':                                         # Clear the cache
        self.cache.clear()
        return self

    @type_safe
    def list_taxonomies(self) -> List__Taxonomy_Ids:                                 # List all cached taxonomy IDs
        result = List__Taxonomy_Ids()
        for taxonomy_id in self.cache.keys():
            result.append(taxonomy_id)
        return result
