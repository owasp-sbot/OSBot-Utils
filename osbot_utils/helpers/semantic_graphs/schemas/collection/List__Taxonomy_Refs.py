# ═══════════════════════════════════════════════════════════════════════════════
# List__Taxonomy_Refs - Typed collection for lists of taxonomy references
# Used by Taxonomy__Registry for registry listing
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref             import Taxonomy_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Taxonomy_Refs(Type_Safe__List):                                          # List of taxonomy references
    expected_type = Taxonomy_Ref
