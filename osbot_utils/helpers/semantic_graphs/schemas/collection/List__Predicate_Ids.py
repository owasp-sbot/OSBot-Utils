# ═══════════════════════════════════════════════════════════════════════════════
# List__Predicate_Ids - Typed collection for lists of predicate identifiers
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id             import Predicate_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                import Type_Safe__List


class List__Predicate_Ids(Type_Safe__List):                                          # List of predicate identifiers
    expected_type = Predicate_Id
