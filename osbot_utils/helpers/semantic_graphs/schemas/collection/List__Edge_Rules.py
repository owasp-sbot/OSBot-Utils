# ═══════════════════════════════════════════════════════════════════════════════
# List__Edge_Rules - Typed collection for edge constraint rules
# Used by Schema__Ontology to define valid edges
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Edge_Rule import Schema__Ontology__Edge_Rule
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                 import Type_Safe__List


class List__Edge_Rules(Type_Safe__List):                                             # List of edge constraint rules
    expected_type = Schema__Ontology__Edge_Rule
