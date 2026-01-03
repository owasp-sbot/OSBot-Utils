# ═══════════════════════════════════════════════════════════════════════════════
# Rule_Set__Utils - Utility operations for rule set evaluation
# Extracted from Schema__Rule_Set to keep schemas as pure data containers
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id           import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set             import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality    import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                               import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                     import type_safe


class Rule_Set__Utils(Type_Safe):                                                    # Utility operations for rule sets

    # ═══════════════════════════════════════════════════════════════════════════════
    # Transitivity Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def is_transitive(self, rule_set   : Schema__Rule_Set         ,
                            source_type: Node_Type_Id             ,
                            verb       : Safe_Str__Ontology__Verb ,
                            target_type: Node_Type_Id             ) -> bool:         # Check if edge is transitive
        for rule in rule_set.transitivity_rules:
            if (rule.source_type == source_type and
                rule.verb        == verb        and
                rule.target_type == target_type):
                return True
        return False

    # ═══════════════════════════════════════════════════════════════════════════════
    # Cardinality Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def get_cardinality(self, rule_set   : Schema__Rule_Set         ,
                              source_type: Node_Type_Id             ,
                              verb       : Safe_Str__Ontology__Verb ,
                              target_type: Node_Type_Id             ) -> Schema__Rule__Cardinality:
        for rule in rule_set.cardinality_rules:                                      # Get cardinality rule if exists
            if (rule.source_type == source_type and
                rule.verb        == verb        and
                rule.target_type == target_type):
                return rule
        return None
