# ═══════════════════════════════════════════════════════════════════════════════
# Taxonomy_Ref - Reference to taxonomy definitions by name
#
# IMPORTANT: This is a REFERENCE (human-readable label like "code_elements")
#            For instance IDs, use Taxonomy_Id
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Ref             import Semantic_Ref


class Taxonomy_Ref(Semantic_Ref):                                                    # Taxonomy reference by name
    pass                                                                             # e.g., "code_elements", "call_flow_taxonomy"
