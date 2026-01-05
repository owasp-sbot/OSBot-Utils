# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Predicates__By_Ref - Typed collection mapping predicate refs to definitions
# Used for lookup by human-readable reference name
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref            import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology__Predicate import Schema__Ontology__Predicate
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class Dict__Predicates__By_Ref(Type_Safe__Dict):                                     # Maps predicate refs to definitions
    expected_key_type   = Predicate_Ref
    expected_value_type = Schema__Ontology__Predicate
