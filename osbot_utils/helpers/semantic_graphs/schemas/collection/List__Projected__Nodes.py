# ═══════════════════════════════════════════════════════════════════════════════
# List__Projected__Nodes - Typed collection for projected nodes
# Used by Projected__Data
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Node   import Schema__Projected__Node
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Projected__Nodes(Type_Safe__List):                                       # List of projected nodes
    expected_type = Schema__Projected__Node
