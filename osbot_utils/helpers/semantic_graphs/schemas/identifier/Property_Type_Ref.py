# ═══════════════════════════════════════════════════════════════════════════════
# Property_Type_Ref - Reference to property types by human-readable label
#
# IMPORTANT: This is a REFERENCE (human-readable label like "integer", "boolean")
#            For instance IDs, use Property_Type_Id
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Ref             import Semantic_Ref


class Property_Type_Ref(Semantic_Ref):                                               # Property type reference by label
    pass                                                                             # e.g., "integer", "boolean", "string", "float"
