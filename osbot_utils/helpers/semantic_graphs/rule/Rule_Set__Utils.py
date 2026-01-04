# ═══════════════════════════════════════════════════════════════════════════════
# Rule_Set__Utils - Operations on Schema__Rule_Set (business logic)
# All operations take rule_set as first parameter - schemas remain pure data
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref            import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set               import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality      import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity     import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                       import type_safe


class Rule_Set__Utils(Type_Safe):                                                     # Operations on rule set schemas

    @type_safe
    def is_transitive(self                              ,
                      rule_set    : Schema__Rule_Set    ,
                      source_type : Node_Type_Ref       ,
                      verb        : Safe_Str__Ontology__Verb,
                      target_type : Node_Type_Ref       ) -> bool:                    # Check if relationship is transitive
        for rule in rule_set.transitivity_rules:
            if (rule.source_type == source_type and
                rule.verb        == verb        and
                rule.target_type == target_type):
                return True
        return False

    @type_safe
    def get_transitivity_rule(self                              ,
                              rule_set    : Schema__Rule_Set    ,
                              source_type : Node_Type_Ref       ,
                              verb        : Safe_Str__Ontology__Verb,
                              target_type : Node_Type_Ref       ) -> Schema__Rule__Transitivity:  # Get transitivity rule
        for rule in rule_set.transitivity_rules:
            if (rule.source_type == source_type and
                rule.verb        == verb        and
                rule.target_type == target_type):
                return rule
        return None

    @type_safe
    def get_cardinality_rule(self                              ,
                             rule_set    : Schema__Rule_Set    ,
                             source_type : Node_Type_Ref       ,
                             verb        : Safe_Str__Ontology__Verb,
                             target_type : Node_Type_Ref       ) -> Schema__Rule__Cardinality:   # Get cardinality rule
        for rule in rule_set.cardinality_rules:
            if (rule.source_type == source_type and
                rule.verb        == verb        and
                rule.target_type == target_type):
                return rule
        return None

    @type_safe
    def has_cardinality_constraint(self                              ,
                                   rule_set    : Schema__Rule_Set    ,
                                   source_type : Node_Type_Ref       ,
                                   verb        : Safe_Str__Ontology__Verb,
                                   target_type : Node_Type_Ref       ) -> bool:       # Check if has cardinality constraint
        return self.get_cardinality_rule(rule_set, source_type, verb, target_type) is not None

    @type_safe
    def validate_cardinality(self                              ,
                             rule_set    : Schema__Rule_Set    ,
                             source_type : Node_Type_Ref       ,
                             verb        : Safe_Str__Ontology__Verb,
                             target_type : Node_Type_Ref       ,
                             count       : int                 ) -> bool:             # Validate count against cardinality
        rule = self.get_cardinality_rule(rule_set, source_type, verb, target_type)
        if rule is None:
            return True                                                               # No constraint = valid
        if count < rule.min_targets:
            return False
        if rule.max_targets is not None and count > rule.max_targets:
            return False
        return True
