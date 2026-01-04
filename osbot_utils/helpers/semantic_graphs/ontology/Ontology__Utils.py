# ═══════════════════════════════════════════════════════════════════════════════
# Ontology__Utils - Operations on Schema__Ontology (business logic)
# All operations take ontology as first parameter - schemas remain pure data
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Node_Type_Refs       import List__Node_Type_Refs
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Ontology__Verbs      import List__Ontology__Verbs
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Valid_Edges          import List__Valid_Edges
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref              import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology             import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Node_Type  import Schema__Ontology__Node_Type
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Valid_Edge           import Schema__Valid_Edge
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb     import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                         import type_safe


class Ontology__Utils(Type_Safe):                                                      # Operations on ontology schemas

    @type_safe
    def get_node_type(self                    ,
                      ontology : Schema__Ontology ,
                      type_ref : Node_Type_Ref    ) -> Schema__Ontology__Node_Type:    # Get node type by ref
        return ontology.node_types.get(type_ref)

    @type_safe
    def has_node_type(self                    ,
                      ontology : Schema__Ontology ,
                      type_ref : Node_Type_Ref    ) -> bool:                           # Check if node type exists
        return type_ref in ontology.node_types

    @type_safe
    def node_type_refs(self                   ,
                       ontology : Schema__Ontology) -> List__Node_Type_Refs:           # All node type refs
        result = List__Node_Type_Refs()
        for type_ref in ontology.node_types.keys():
            result.append(type_ref)
        return result

    @type_safe
    def all_verbs(self                        ,
                  ontology : Schema__Ontology ) -> List__Ontology__Verbs:              # All verbs from all relationships
        result = List__Ontology__Verbs()
        for node_type in ontology.node_types.values():
            for verb in node_type.relationships.keys():
                if verb not in result:
                    result.append(verb)
        return result

    @type_safe
    def all_valid_edges(self                  ,
                        ontology : Schema__Ontology) -> List__Valid_Edges:             # All valid edge combinations
        result = List__Valid_Edges()
        for source_ref, node_type in ontology.node_types.items():
            for verb, relationship in node_type.relationships.items():
                for target_ref in relationship.targets:
                    valid_edge = Schema__Valid_Edge(source_type = source_ref  ,
                                                    verb        = verb        ,
                                                    target_type = target_ref  )
                    result.append(valid_edge)
        return result

    @type_safe
    def is_valid_edge(self                         ,
                      ontology    : Schema__Ontology        ,
                      source_type : Node_Type_Ref           ,
                      verb        : Safe_Str__Ontology__Verb,
                      target_type : Node_Type_Ref           ) -> bool:                 # Check if edge is valid
        node_type = self.get_node_type(ontology, source_type)
        if node_type is None:
            return False
        relationship = node_type.relationships.get(verb)
        if relationship is None:
            return False
        return target_type in relationship.targets

    @type_safe
    def get_inverse_verb(self                      ,
                         ontology    : Schema__Ontology        ,
                         source_type : Node_Type_Ref           ,
                         verb        : Safe_Str__Ontology__Verb) -> Safe_Str__Ontology__Verb:  # Get inverse verb
        node_type = self.get_node_type(ontology, source_type)
        if node_type is None:
            return None
        relationship = node_type.relationships.get(verb)
        if relationship is None:
            return None
        return relationship.inverse

    @type_safe
    def valid_targets(self                         ,
                      ontology    : Schema__Ontology        ,
                      source_type : Node_Type_Ref           ,
                      verb        : Safe_Str__Ontology__Verb) -> List__Node_Type_Refs: # Valid targets for edge
        node_type = self.get_node_type(ontology, source_type)
        if node_type is None:
            return List__Node_Type_Refs()
        relationship = node_type.relationships.get(verb)
        if relationship is None:
            return List__Node_Type_Refs()
        return relationship.targets
