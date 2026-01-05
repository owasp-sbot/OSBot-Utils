# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Projected_Properties - Maps property name refs to values in projections
# Used by Schema__Projected__Node and Schema__Projected__Edge
# Human-readable: uses refs (not IDs) for keys
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Ref       import Property_Name_Ref
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict


class Dict__Projected_Properties(Type_Safe__Dict):                                   # Maps property name refs to values
    expected_key_type   = Property_Name_Ref
    expected_value_type = Safe_Str__Text
