# ═══════════════════════════════════════════════════════════════════════════════
# List__Ontology_Ids - Typed collection for lists of ontology instance IDs
# Used by Ontology__Registry for ID listing
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id              import Ontology_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Ontology_Ids(Type_Safe__List):                                           # List of ontology instance IDs
    expected_type = Ontology_Id
