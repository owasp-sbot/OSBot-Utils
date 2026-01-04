# ═══════════════════════════════════════════════════════════════════════════════
# List__Ontology_Refs - Typed collection for lists of ontology references
# Used by Ontology__Registry for registry listing
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref             import Ontology_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Ontology_Refs(Type_Safe__List):                                          # List of ontology references
    expected_type = Ontology_Ref
