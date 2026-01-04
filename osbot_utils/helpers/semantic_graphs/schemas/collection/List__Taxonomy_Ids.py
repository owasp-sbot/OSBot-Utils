# ═══════════════════════════════════════════════════════════════════════════════
# List__Taxonomy_Ids - Typed collection for lists of taxonomy identifiers
# Used by Taxonomy__Registry for registry listing
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id              import Taxonomy_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Taxonomy_Ids(Type_Safe__List):                                           # List of taxonomy identifiers
    expected_type = Taxonomy_Id
