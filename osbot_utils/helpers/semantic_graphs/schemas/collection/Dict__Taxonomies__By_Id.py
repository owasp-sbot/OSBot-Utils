# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Taxonomies__By_Id - Typed collection mapping taxonomy IDs to taxonomies
# Used by Taxonomy__Registry for lookup by instance ID
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Id              import Taxonomy_Id
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy           import Schema__Taxonomy
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class Dict__Taxonomies__By_Id(Type_Safe__Dict):                                      # Maps taxonomy IDs to taxonomy objects
    expected_key_type   = Taxonomy_Id
    expected_value_type = Schema__Taxonomy
