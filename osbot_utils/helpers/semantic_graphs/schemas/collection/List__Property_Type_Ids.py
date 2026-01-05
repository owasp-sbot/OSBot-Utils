# ═══════════════════════════════════════════════════════════════════════════════
# List__Property_Type_Ids - Typed collection for lists of property type IDs
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Id        import Property_Type_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List               import Type_Safe__List


class List__Property_Type_Ids(Type_Safe__List):                                      # List of property type identifiers
    expected_type = Property_Type_Id
