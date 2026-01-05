# ═══════════════════════════════════════════════════════════════════════════════
# Rule_Set_Ref - Reference to rule set definitions by name
#
# IMPORTANT: This is a REFERENCE (human-readable label like "call_flow_rules")
#            For instance IDs, use Rule_Set_Id
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Ref             import Semantic_Ref


class Rule_Set_Ref(Semantic_Ref):                                                    # Rule set reference by name
    pass                                                                             # e.g., "call_flow_rules", "python_rules"
