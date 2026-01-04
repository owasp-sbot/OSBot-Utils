# ═══════════════════════════════════════════════════════════════════════════════
# List__Taxonomy__Categories - Typed collection for lists of taxonomy categories
# Used by Taxonomy__Utils for hierarchy navigation
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy__Category import Schema__Taxonomy__Category
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Taxonomy__Categories(Type_Safe__List):                                   # List of taxonomy categories
    expected_type = Schema__Taxonomy__Category
