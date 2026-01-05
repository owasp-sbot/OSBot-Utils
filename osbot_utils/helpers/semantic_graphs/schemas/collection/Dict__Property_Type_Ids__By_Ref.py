# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Property_Type_Ids__By_Ref - Maps property type refs to their IDs
# Used by Schema__Projected__References for correlation lookups
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Id        import Property_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Ref       import Property_Type_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict


class Dict__Property_Type_Ids__By_Ref(Type_Safe__Dict):                              # Maps refs to IDs for property types
    expected_key_type   = Property_Type_Ref
    expected_value_type = Property_Type_Id
