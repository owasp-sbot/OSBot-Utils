from typing                                                                              import List, Tuple
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Types__By_Id      import Dict__Node_Types__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                 import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                  import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id                  import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Relationship import Schema__Ontology__Relationship
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                           import type_safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text             import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version          import Safe_Str__Version

# refactor out methods

class Schema__Ontology(Type_Safe):                                                       # Complete ontology definition
    ontology_id  : Ontology_Id                                                           # Unique identifier
    version      : Safe_Str__Version             = Safe_Str__Version('1.0.0')            # Semantic version
    description  : Safe_Str__Text                                                        # What this ontology models
    taxonomy_ref : Taxonomy_Id                                                           # Optional taxonomy reference
    node_types   : Dict__Node_Types__By_Id                                               # type_id → definition

    @type_safe
    def valid_edge(self, source_type: Node_Type_Id,
                   verb: Safe_Str__Ontology__Verb,
                   target_type: Node_Type_Id
              ) -> bool:
        node_type = self.node_types.get(source_type)
        if not node_type:
            return False
        relationship = node_type.relationships.get(verb)
        if not relationship:
            return False
        return target_type in relationship.targets

    @type_safe
    def get_inverse_verb(self,
                         source_type: Node_Type_Id,
                         verb: Safe_Str__Ontology__Verb
                    ) -> Safe_Str__Ontology__Verb:
        node_type = self.node_types.get(source_type)
        if not node_type:
            return None
        relationship = node_type.relationships.get(verb)
        if not relationship:
            return None
        return relationship.inverse

    @type_safe
    def edge_forward_name(self,
                          source_type: Node_Type_Id,
                          verb: Safe_Str__Ontology__Verb,
                          target_type: Node_Type_Id
                     ) -> str:                                      # todo: convert to type safe primitive
        return f"{source_type}_{verb}_{target_type}"

    @type_safe
    def edge_inverse_name(self,
                          source_type: Node_Type_Id,
                          verb: Safe_Str__Ontology__Verb,
                          target_type: Node_Type_Id
                     ) -> str:                                      # todo: convert to type safe primitive
        inverse_verb = self.get_inverse_verb(source_type, verb)
        if inverse_verb:
            return f"{target_type}_{inverse_verb}_{source_type}"
        return ""

    # fix return type
    @type_safe
    def all_valid_edges(self) -> List[Tuple[Node_Type_Id, Safe_Str__Ontology__Verb, Node_Type_Id]]:
        edges = []
        for source_id, node_type in self.node_types.items():
            for verb, rel in node_type.relationships.items():
                for target_id in rel.targets:
                    edges.append((source_id, verb, target_id))
        return edges

    def node_type_ids(self) -> List[Node_Type_Id]:
        return list(self.node_types.keys())

    def verbs_for_node_type(self, node_type_id: Node_Type_Id) -> List[Safe_Str__Ontology__Verb]:
        node_type = self.node_types.get(node_type_id)
        if not node_type:
            return []
        return list(node_type.relationships.keys())

    def targets_for_verb(self, node_type_id: Node_Type_Id, verb: Safe_Str__Ontology__Verb) -> List[Node_Type_Id]:
        node_type = self.node_types.get(node_type_id)
        if not node_type:
            return []
        relationship = node_type.relationships.get(verb)
        if not relationship:
            return []
        return list(relationship.targets)