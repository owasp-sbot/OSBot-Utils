# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Taxonomies__By_Ref - Typed collection mapping taxonomy refs to taxonomies
# Used by Taxonomy__Registry for lookup by reference name
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Taxonomy_Ref             import Taxonomy_Ref
from osbot_utils.helpers.semantic_graphs.schemas.taxonomy.Schema__Taxonomy           import Schema__Taxonomy
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class Dict__Taxonomies__By_Ref(Type_Safe__Dict):                                     # Maps taxonomy refs to taxonomy objects
    expected_key_type   = Taxonomy_Ref
    expected_value_type = Schema__Taxonomy
