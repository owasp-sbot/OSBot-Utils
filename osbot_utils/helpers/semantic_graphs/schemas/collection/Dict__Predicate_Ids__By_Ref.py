# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Predicate_Ids__By_Ref - Maps predicate refs to their IDs
# Used by Projected__References for correlation lookups
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id             import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref            import Predicate_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                import Type_Safe__Dict


class Dict__Predicate_Ids__By_Ref(Type_Safe__Dict):                                  # Maps refs to IDs for predicates
    expected_key_type   = Predicate_Ref
    expected_value_type = Predicate_Id
