# ═══════════════════════════════════════════════════════════════════════════════
# List__Rules__Required_Edge_Property - Typed collection for edge property rules
# Used by Schema__Rule_Set
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Required_Edge_Property import Schema__Rule__Required_Edge_Property
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                      import Type_Safe__List


class List__Rules__Required_Edge_Property(Type_Safe__List):                          # List of required edge property rules
    expected_type = Schema__Rule__Required_Edge_Property
