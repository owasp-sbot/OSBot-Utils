# ═══════════════════════════════════════════════════════════════════════════════
# Rule__Engine - Load rule sets and apply to graphs
# Refactored to use osbot-utils file methods and proper typed collections
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Rule_Sets__By_Id     import Dict__Rule_Sets__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set                 import Schema__Rule_Set
from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path      import Safe_Str__File__Path
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                         import type_safe
from osbot_utils.utils.Json                                                            import json_file_load


class Rule__Engine(Type_Safe):                                                       # Load rule sets and apply to graphs
    cache : Dict__Rule_Sets__By_Id                                                   # Cached rule sets by ID

    @type_safe
    def load_from_file(self, file_path: Safe_Str__File__Path) -> Schema__Rule_Set:   # Load rule set from JSON file
        data = json_file_load(file_path)
        if data == {}:                                                               # if file doesn't exist, could not be parsed or had no content
            return None
        return self.load_from_dict(data)

    @type_safe
    def load_from_dict(self, data: dict) -> Schema__Rule_Set:                        # Load rule set from dictionary
        rule_set = self.parse_rule_set(data)
        self.cache[rule_set.rule_set_id] = rule_set
        return rule_set

    @type_safe
    def parse_rule_set(self, data: dict) -> Schema__Rule_Set:                        # Parse rule set from dict
        return Schema__Rule_Set.from_json(data)

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
