import json
from typing                                                                             import Dict, Optional
from pathlib                                                                            import Path
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                 import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                 import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                  import Schema__Rule_Set
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality         import Schema__Rule__Cardinality
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity        import Schema__Rule__Transitivity
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb      import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path       import Safe_Str__File__Path


# todo: fix cache type
class Rule__Engine(Type_Safe):                                                       # Load rule sets and apply to graphs
    cache : Dict[Rule_Set_Id, Schema__Rule_Set]                                              # Cached rule sets by ID

    # todo: use osbot-utils file methods
    def load_from_file(self, file_path: Safe_Str__File__Path) -> Schema__Rule_Set:                    # Load rule set from JSON file
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Rule set file not found: {file_path}")

        with open(path, 'r') as f:
            data = json.load(f)

        rule_set = self.parse_rule_set(data)
        self.cache[rule_set.rule_set_id] = rule_set
        return rule_set

    def load_from_dict(self, data: dict) -> Schema__Rule_Set:                        # Load rule set from dictionary
        rule_set = self.parse_rule_set(data)
        self.cache[rule_set.rule_set_id] = rule_set
        return rule_set

    def parse_rule_set(self, data: dict) -> Schema__Rule_Set:                        # Parse rule set from dict
        transitivity_rules = []
        for rule_data in data.get('transitivity_rules', []):
            rule = Schema__Rule__Transitivity(
                source_type = Node_Type_Id(rule_data.get('source_type', ''))         ,
                verb        = Safe_Str__Ontology__Verb(rule_data.get('verb', ''))    ,
                target_type = Node_Type_Id(rule_data.get('target_type', ''))         ,
            )
            transitivity_rules.append(rule)

        cardinality_rules = []
        for rule_data in data.get('cardinality_rules', []):
            max_targets = rule_data.get('max_targets')
            rule = Schema__Rule__Cardinality(
                source_type = Node_Type_Id(rule_data.get('source_type', ''))         ,
                verb        = Safe_Str__Ontology__Verb(rule_data.get('verb', ''))    ,
                target_type = Node_Type_Id(rule_data.get('target_type', ''))         ,
                min_targets = rule_data.get('min_targets', 0)                        ,
                max_targets = max_targets                                            ,
                description = rule_data.get('description', '')                       ,
            )
            cardinality_rules.append(rule)

        return Schema__Rule_Set(
            rule_set_id        = Rule_Set_Id(data.get('rule_set_id', ''))             ,
            ontology_ref       = Ontology_Id(data.get('ontology_ref', ''))            ,
            version            = data.get('version', '1.0.0')                        ,
            description        = data.get('description', '')                         ,
            transitivity_rules = transitivity_rules                                  ,
            cardinality_rules  = cardinality_rules                                   ,
        )

    def get(self, rule_set_id: Rule_Set_Id) -> Schema__Rule_Set:                   # Get cached rule set by ID
        return self.cache.get(rule_set_id)

    def register(self, rule_set: Schema__Rule_Set):                                  # Manually register a rule set
        self.cache[rule_set.rule_set_id] = rule_set

    def clear(self):                                                                 # Clear the cache
        self.cache.clear()
        return self

    def list_rule_sets(self) -> list:                                                # List all cached rule set IDs
        return list(self.cache.keys())
