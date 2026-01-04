# ═══════════════════════════════════════════════════════════════════════════════
# Ontology_Ref - Reference to ontology definitions by name
#
# IMPORTANT: This is a REFERENCE (human-readable label like "call_flow")
#            For instance IDs, use Ontology_Id
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Ref             import Semantic_Ref


class Ontology_Ref(Semantic_Ref):                                                    # Ontology reference by name
    pass                                                                             # e.g., "call_flow", "code_structure"
