# ═══════════════════════════════════════════════════════════════════════════════
# Ontology_Id - Instance identifier for ontology objects
#
# IMPORTANT: This is an INSTANCE ID (unique per ontology instance)
#            For human-readable references, use Ontology_Ref
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Id              import Semantic_Id


class Ontology_Id(Semantic_Id):                                                      # Ontology instance identifier
    pass                                                                             # Created via Ontology_Id(Obj_Id()) or Ontology_Id(Obj_Id.from_seed(...))
