# ═══════════════════════════════════════════════════════════════════════════════
# List__Rules__Required_Node_Property - Typed collection for node property rules
# Used by Schema__Rule_Set
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Node_Property import Schema__Rule__Required_Node_Property
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                      import Type_Safe__List


class List__Rules__Required_Node_Property(Type_Safe__List):                          # List of required node property rules
    expected_type = Schema__Rule__Required_Node_Property
