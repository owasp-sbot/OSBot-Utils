# ═══════════════════════════════════════════════════════════════════════════════
# List__Property_Name_Ids - Typed collection for lists of property name IDs
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id        import Property_Name_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List               import Type_Safe__List


class List__Property_Name_Ids(Type_Safe__List):                                      # List of property name identifiers
    expected_type = Property_Name_Id
