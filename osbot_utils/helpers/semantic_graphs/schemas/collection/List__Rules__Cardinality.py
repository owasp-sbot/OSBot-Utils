# ═══════════════════════════════════════════════════════════════════════════════
# List__Rules__Cardinality - Typed collection for cardinality rules
# Used by Schema__Rule_Set
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.rule.Schema__Rule__Cardinality import Schema__Rule__Cardinality
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List           import Type_Safe__List


class List__Rules__Cardinality(Type_Safe__List):                                     # List of cardinality rules
    expected_type = Schema__Rule__Cardinality
