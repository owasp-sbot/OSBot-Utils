from typing                                                                                 import List
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id        import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Ontologies__By_Id        import Dict__Ontologies__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Node_Type_Ids            import List__Node_Type_Ids
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                   import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                    import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology                  import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type       import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship    import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb          import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path           import Safe_Str__File__Path
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                              import type_safe
from osbot_utils.utils.Files                                                                import file_exists, file_contents
from osbot_utils.utils.Json                                                                 import json_parse


class Ontology__Registry(Type_Safe):                                                     # Load and cache ontologies from JSON
    cache : Dict__Ontologies__By_Id

    # todo: fix to use osbot-utils file and json methods
    @type_safe
    def load_from_file(self, file_path: Safe_Str__File__Path) -> Schema__Ontology:
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
    def load_from_dict(self, data: dict) -> Schema__Ontology:
        ontology = self.parse_ontology(data)
        self.cache[ontology.ontology_id] = ontology
        return ontology

    @type_safe
    def parse_ontology(self, data: dict) -> Schema__Ontology:
        node_types = Dict__Node_Types__By_Id()

        for type_id, type_data in data.get('node_types', {}).items():
            relationships = Schema__Ontology__Node_Type().relationships

            for verb, rel_data in type_data.get('relationships', {}).items():
                targets      = List__Node_Type_Ids([Node_Type_Id(t) for t in rel_data.get('targets', [])])
                relationship = Schema__Ontology__Relationship(inverse = Safe_Str__Ontology__Verb(rel_data.get('inverse', '')),
                                                              targets = targets                                             )
                relationships[verb] = relationship

            node_type = Schema__Ontology__Node_Type(description   = type_data.get('description', '') ,
                                                    relationships = relationships                    ,
                                                    taxonomy_ref  = type_data.get('taxonomy_ref', ''))
            node_types[type_id] = node_type

        return Schema__Ontology(ontology_id  = Ontology_Id(data.get('ontology_id', '')),
                                version      = data.get('version', '1.0.0')            ,
                                description  = data.get('description', '')             ,
                                taxonomy_ref = data.get('taxonomy_ref', '')            ,
                                node_types   = node_types                              )

    @type_safe
    def get(self, ontology_id: Ontology_Id) -> Schema__Ontology:
        return self.cache.get(ontology_id)

    @type_safe
    def register(self, ontology: Schema__Ontology) -> None:
        self.cache[ontology.ontology_id] = ontology

    def clear(self) -> None:
        self.cache.clear()

    def list_ontologies(self) -> List[Ontology_Id]:
        return list(self.cache.keys())