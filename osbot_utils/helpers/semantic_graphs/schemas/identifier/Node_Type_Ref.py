# ═══════════════════════════════════════════════════════════════════════════════
# Node_Type_Ref - Reference to node types defined in ontology
#
# IMPORTANT: This is a REFERENCE (human-readable label like "class", "method")
#            Node types are defined in ontology and referenced by this label
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Ref             import Semantic_Ref


class Node_Type_Ref(Semantic_Ref):                                                   # Node type reference by name
    pass                                                                             # e.g., "class", "method", "function", "package"
