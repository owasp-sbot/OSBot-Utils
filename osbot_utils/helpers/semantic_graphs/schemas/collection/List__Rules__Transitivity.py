# ═══════════════════════════════════════════════════════════════════════════════
# List__Rules__Transitivity - Typed collection for transitivity rules
# Used by Schema__Rule_Set
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Transitivity import Schema__Rule__Transitivity
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List            import Type_Safe__List


class List__Rules__Transitivity(Type_Safe__List):                                    # List of transitivity rules
    expected_type = Schema__Rule__Transitivity
