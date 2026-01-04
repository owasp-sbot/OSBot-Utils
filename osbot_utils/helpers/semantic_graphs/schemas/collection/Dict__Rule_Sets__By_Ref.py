# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Rule_Sets__By_Ref - Typed collection mapping rule set refs to rule sets
# Used by Rule__Engine for lookup by reference name
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref             import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set               import Schema__Rule_Set
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class Dict__Rule_Sets__By_Ref(Type_Safe__Dict):                                      # Maps rule set refs to rule set objects
    expected_key_type   = Rule_Set_Ref
    expected_value_type = Schema__Rule_Set
