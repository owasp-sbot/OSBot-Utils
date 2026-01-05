# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Predicates__By_Id - Typed collection mapping predicate IDs to definitions
# Used by Schema__Ontology for predicate storage
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id             import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Predicate import Schema__Ontology__Predicate
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class Dict__Predicates__By_Id(Type_Safe__Dict):                                      # Maps predicate IDs to definitions
    expected_key_type   = Predicate_Id
    expected_value_type = Schema__Ontology__Predicate
