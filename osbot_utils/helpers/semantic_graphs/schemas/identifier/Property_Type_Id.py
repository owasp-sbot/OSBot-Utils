# ═══════════════════════════════════════════════════════════════════════════════
# Property_Type_Id - Instance identifier for property type objects
#
# IMPORTANT: This is an INSTANCE ID (unique per property type instance)
#            For human-readable references, use Property_Type_Ref
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Semantic_Id              import Semantic_Id


class Property_Type_Id(Semantic_Id):                                                 # Property type instance identifier
    pass                                                                             # Created via Property_Type_Id(Obj_Id()) or Property_Type_Id(Obj_Id.from_seed(...))
