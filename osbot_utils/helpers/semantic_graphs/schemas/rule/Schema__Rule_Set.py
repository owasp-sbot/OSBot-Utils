from typing                                                                          import List

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id              import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id              import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality      import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity     import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text         import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version      import Safe_Str__Version
from osbot_utils.type_safe.type_safe_core.decorators.type_safe import type_safe


# refactor out methods

class Schema__Rule_Set(Type_Safe):                                                   # Collection of rules for a domain
    rule_set_id        : Rule_Set_Id                                                 # Unique identifier
    ontology_ref       : Ontology_Id                                                 # Which ontology this applies to
    version            : Safe_Str__Version       = Safe_Str__Version('1.0.0')        # Semantic version
    description        : Safe_Str__Text          = Safe_Str__Text('')                # What rules this contains
    transitivity_rules : List[Schema__Rule__Transitivity]                            # Transitive relationships
    cardinality_rules  : List[Schema__Rule__Cardinality]                             # Cardinality constraints

    @type_safe
    def is_transitive(self,
                      source_type: Node_Type_Id             ,
                      verb       : Safe_Str__Ontology__Verb ,
                      target_type: Node_Type_Id             ) -> bool:  # Check if edge is transitive
        for rule in self.transitivity_rules:
            if (rule.source_type == source_type and
                rule.verb        == verb        and
                rule.target_type == target_type):
                return True
        return False

    def get_cardinality(self,
                        source_type : Node_Type_Id,
                        verb        : Safe_Str__Ontology__Verb,                           # Get cardinality rule if exists
                        target_type : Node_Type_Id) -> Schema__Rule__Cardinality:
        for rule in self.cardinality_rules:
            if (rule.source_type == source_type and
                rule.verb        == verb and
                rule.target_type == target_type):
                return rule
        return None
