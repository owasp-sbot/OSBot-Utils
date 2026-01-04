# ═══════════════════════════════════════════════════════════════════════════════
# List__Rule_Set_Ids - Typed collection for lists of rule set identifiers
# Used by Rule__Engine for registry listing
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id              import Rule_Set_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Rule_Set_Ids(Type_Safe__List):                                           # List of rule set identifiers
    expected_type = Rule_Set_Id
