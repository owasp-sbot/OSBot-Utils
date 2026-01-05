# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Property_Name_Ids__By_Ref - Maps property name refs to their IDs
# Used by Schema__Projected__References for correlation lookups
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id        import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Ref       import Property_Name_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict


class Dict__Property_Name_Ids__By_Ref(Type_Safe__Dict):                              # Maps refs to IDs for property names
    expected_key_type   = Property_Name_Ref
    expected_value_type = Property_Name_Id
