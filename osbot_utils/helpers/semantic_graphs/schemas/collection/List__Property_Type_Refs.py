# ═══════════════════════════════════════════════════════════════════════════════
# List__Property_Type_Refs - Typed collection for lists of property type refs
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Type_Ref       import Property_Type_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List               import Type_Safe__List


class List__Property_Type_Refs(Type_Safe__List):                                     # List of property type references
    expected_type = Property_Type_Ref
