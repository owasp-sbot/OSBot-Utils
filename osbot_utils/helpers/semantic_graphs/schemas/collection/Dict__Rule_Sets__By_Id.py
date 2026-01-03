# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Rule_Sets__By_Id - Typed collection mapping Rule Set IDs to rule sets
# Used by Rule__Engine for caching
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule_Set  import Schema__Rule_Set
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict   import Type_Safe__Dict


class Dict__Rule_Sets__By_Id(Type_Safe__Dict):                                       # Maps rule set IDs to rule sets
    expected_key_type   = Rule_Set_Id
    expected_value_type = Schema__Rule_Set
