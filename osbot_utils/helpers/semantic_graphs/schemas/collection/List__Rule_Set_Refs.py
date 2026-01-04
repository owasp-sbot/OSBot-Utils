# ═══════════════════════════════════════════════════════════════════════════════
# List__Rule_Set_Refs - Typed collection for lists of rule set references
# Used by Rule__Engine for registry listing
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref             import Rule_Set_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Rule_Set_Refs(Type_Safe__List):                                          # List of rule set references
    expected_type = Rule_Set_Ref
