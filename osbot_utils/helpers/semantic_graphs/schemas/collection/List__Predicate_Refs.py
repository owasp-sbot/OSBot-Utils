# ═══════════════════════════════════════════════════════════════════════════════
# List__Predicate_Refs - Typed collection for lists of predicate references
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref            import Predicate_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Predicate_Refs(Type_Safe__List):                                         # List of predicate references
    expected_type = Predicate_Ref
