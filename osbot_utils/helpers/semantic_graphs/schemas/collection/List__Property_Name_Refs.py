# ═══════════════════════════════════════════════════════════════════════════════
# List__Property_Name_Refs - Typed collection for lists of property name refs
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Ref       import Property_Name_Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List               import Type_Safe__List


class List__Property_Name_Refs(Type_Safe__List):                                     # List of property name references
    expected_type = Property_Name_Ref
