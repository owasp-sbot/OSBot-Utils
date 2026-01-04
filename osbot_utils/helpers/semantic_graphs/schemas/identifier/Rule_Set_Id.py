# ═══════════════════════════════════════════════════════════════════════════════
# Rule_Set_Id - Instance identifier for rule set objects
#
# IMPORTANT: This is an INSTANCE ID (unique per rule set instance)
#            For human-readable references, use Rule_Set_Ref
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Id              import Semantic_Id


class Rule_Set_Id(Semantic_Id):                                                      # Rule set instance identifier
    pass                                                                             # Created via Rule_Set_Id(Obj_Id()) or Rule_Set_Id(Obj_Id.from_seed(...))
