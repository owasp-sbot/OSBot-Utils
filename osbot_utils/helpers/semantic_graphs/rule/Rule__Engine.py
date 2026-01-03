# ═══════════════════════════════════════════════════════════════════════════════
# Rule__Engine - Load rule sets and apply to graphs
# Refactored to use osbot-utils file methods and proper typed collections
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Rule_Sets__By_Id     import Dict__Rule_Sets__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id               import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                 import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality        import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity       import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb     import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                         import type_safe
from osbot_utils.utils.Files                                                           import file_exists, file_contents
from osbot_utils.utils.Json                                                            import json_parse


class Rule__Engine(Type_Safe):                                                       # Load rule sets and apply to graphs
    cache : Dict__Rule_Sets__By_Id                                                   # Cached rule sets by ID

    @type_safe
    def load_from_file(self, file_path: Safe_Str__File__Path) -> Schema__Rule_Set:   # Load rule set from JSON file
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
    def load_from_dict(self, data: dict) -> Schema__Rule_Set:                        # Load rule set from dictionary
        rule_set = self.parse_rule_set(data)
        self.cache[rule_set.rule_set_id] = rule_set
        return rule_set

    @type_safe
    def parse_rule_set(self, data: dict) -> Schema__Rule_Set:                        # Parse rule set from dict
        transitivity_rules = []
        for rule_data in data.get('transitivity_rules', []):
            rule = Schema__Rule__Transitivity(source_type = Node_Type_Id(rule_data.get('source_type', '')),
                                              verb        = Safe_Str__Ontology__Verb(rule_data.get('verb', '')),
                                              target_type = Node_Type_Id(rule_data.get('target_type', '')))
            transitivity_rules.append(rule)

        cardinality_rules = []
        for rule_data in data.get('cardinality_rules', []):
            max_targets = rule_data.get('max_targets')
            rule = Schema__Rule__Cardinality(source_type = Node_Type_Id(rule_data.get('source_type', '')),
                                             verb        = Safe_Str__Ontology__Verb(rule_data.get('verb', '')),
                                             target_type = Node_Type_Id(rule_data.get('target_type', '')),
                                             min_targets = rule_data.get('min_targets', 0)                    ,
                                             max_targets = max_targets                                        ,
                                             description = rule_data.get('description', '')                   )
            cardinality_rules.append(rule)

        return Schema__Rule_Set(rule_set_id        = Rule_Set_Id(data.get('rule_set_id', '')),
                                ontology_ref       = Ontology_Id(data.get('ontology_ref', '')),
                                version            = data.get('version', '1.0.0')            ,
                                description        = data.get('description', '')             ,
                                transitivity_rules = transitivity_rules                      ,
                                cardinality_rules  = cardinality_rules                       )

    @type_safe
    def get(self, rule_set_id: Rule_Set_Id) -> Schema__Rule_Set:                     # Get cached rule set by ID
        return self.cache.get(rule_set_id)

    @type_safe
    def register(self, rule_set: Schema__Rule_Set) -> None:                          # Manually register a rule set
        self.cache[rule_set.rule_set_id] = rule_set

    def clear(self) -> 'Rule__Engine':                                               # Clear the cache
        self.cache.clear()
        return self

    def list_rule_sets(self) -> list:                                                # List all cached rule set IDs
        return list(self.cache.keys())
