# ═══════════════════════════════════════════════════════════════════════════════
# Predicate_Id - Instance identifier for predicate objects
#
# IMPORTANT: This is an INSTANCE ID (unique per predicate instance)
#            For human-readable references, use Predicate_Ref
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Id              import Semantic_Id


class Predicate_Id(Semantic_Id):                                                     # Predicate instance identifier
    pass                                                                             # Created via Predicate_Id(Obj_Id()) or Predicate_Id(Obj_Id.from_seed(...))
