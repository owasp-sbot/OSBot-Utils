# ═══════════════════════════════════════════════════════════════════════════════
# Category_Ref - Reference to taxonomy categories by name
#
# IMPORTANT: This is a REFERENCE (human-readable label like "container", "callable")
#            Categories are identified by their ref within a taxonomy
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Ref             import Semantic_Ref


class Category_Ref(Semantic_Ref):                                                    # Category reference by name
    pass                                                                             # e.g., "container", "callable", "code_unit"
