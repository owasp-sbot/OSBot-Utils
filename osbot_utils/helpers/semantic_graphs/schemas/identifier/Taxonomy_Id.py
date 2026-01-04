# ═══════════════════════════════════════════════════════════════════════════════
# Taxonomy_Id - Instance identifier for taxonomy objects
#
# IMPORTANT: This is an INSTANCE ID (unique per taxonomy instance)
#            For human-readable references, use Taxonomy_Ref
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Id              import Semantic_Id


class Taxonomy_Id(Semantic_Id):                                                      # Taxonomy instance identifier
    pass                                                                             # Created via Taxonomy_Id(Obj_Id()) or Taxonomy_Id(Obj_Id.from_seed(...))
