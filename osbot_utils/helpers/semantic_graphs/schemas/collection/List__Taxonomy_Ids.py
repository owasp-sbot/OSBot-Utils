# ═══════════════════════════════════════════════════════════════════════════════
# List__Taxonomy_Ids - Typed collection for lists of taxonomy instance IDs
# Used by Taxonomy__Registry for ID listing
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id              import Taxonomy_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Taxonomy_Ids(Type_Safe__List):                                           # List of taxonomy instance IDs
    expected_type = Taxonomy_Id
