# ═══════════════════════════════════════════════════════════════════════════════
# List__Projected__Edges - Typed collection for projected edges
# Used by Projected__Data
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Edge   import Schema__Projected__Edge
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Projected__Edges(Type_Safe__List):                                       # List of projected edges
    expected_type = Schema__Projected__Edge
