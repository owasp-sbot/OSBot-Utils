# ═══════════════════════════════════════════════════════════════════════════════
# Predicate_Ref - Reference to predicate definitions by name
#
# IMPORTANT: This is a REFERENCE (human-readable label like "calls", "contains")
#            For instance IDs, use Predicate_Id
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Ref             import Semantic_Ref


class Predicate_Ref(Semantic_Ref):                                                   # Predicate reference by name
    pass                                                                             # e.g., "calls", "contains", "inherits_from"
