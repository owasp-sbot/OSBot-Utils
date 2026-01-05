# ═══════════════════════════════════════════════════════════════════════════════
# Property_Name_Ref - Reference to property names by human-readable label
#
# IMPORTANT: This is a REFERENCE (human-readable label like "line_number")
#            For instance IDs, use Property_Name_Id
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Ref             import Semantic_Ref


class Property_Name_Ref(Semantic_Ref):                                               # Property name reference by label
    pass                                                                             # e.g., "line_number", "is_async", "call_count"
