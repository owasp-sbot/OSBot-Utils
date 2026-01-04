# ═══════════════════════════════════════════════════════════════════════════════
# Ontology__Registry - Load and cache ontologies from JSON
# Refactored to use osbot-utils file methods and proper typed collections
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Ontologies__By_Id  import Dict__Ontologies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Ontology_Ids       import List__Ontology_Ids
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id              import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology           import Schema__Ontology
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path    import Safe_Str__File__Path
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                       import type_safe
from osbot_utils.utils.Json                                                          import json_file_load


class Ontology__Registry(Type_Safe):                                                 # Load and cache ontologies from JSON
    cache : Dict__Ontologies__By_Id                                                  # Cached ontologies by ID

    @type_safe
    def load_from_file(self, file_path: Safe_Str__File__Path) -> Schema__Ontology:   # Load ontology from JSON file
        data = json_file_load(file_path)
        if data == {}:                                                               # If file doesn't exist or parse failed
            return None
        return self.load_from_dict(data)

    @type_safe
    def load_from_dict(self, data: dict) -> Schema__Ontology:                        # Load ontology from dictionary
        ontology = self.parse_ontology(data)
        if ontology:
            self.cache[ontology.ontology_id] = ontology
        return ontology

    @type_safe
    def parse_ontology(self, data: dict) -> Schema__Ontology:                        # Parse ontology from dict
        return Schema__Ontology.from_json(data)

    @type_safe
    def get(self, ontology_id: Ontology_Id) -> Schema__Ontology:                     # Get cached ontology by ID
        return self.cache.get(ontology_id)

    @type_safe
    def register(self, ontology: Schema__Ontology) -> None:                          # Manually register an ontology
        self.cache[ontology.ontology_id] = ontology

    @type_safe
    def clear(self) -> None:                                                         # Clear the cache
        self.cache.clear()

    @type_safe
    def list_ontologies(self) -> List__Ontology_Ids:                                 # List all cached ontology IDs
        result = List__Ontology_Ids()
        for ontology_id in self.cache.keys():
            result.append(ontology_id)
        return result
