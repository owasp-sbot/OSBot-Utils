# ═══════════════════════════════════════════════════════════════════════════════
# Property_Name_Id - Instance identifier for property name objects
#
# IMPORTANT: This is an INSTANCE ID (unique per property name instance)
#            For human-readable references, use Property_Name_Ref
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Id              import Semantic_Id


class Property_Name_Id(Semantic_Id):                                                 # Property name instance identifier
    pass                                                                             # Created via Property_Name_Id(Obj_Id()) or Property_Name_Id(Obj_Id.from_seed(...))
