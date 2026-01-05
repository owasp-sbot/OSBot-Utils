# ═══════════════════════════════════════════════════════════════════════════════
# Dict__Node_Properties - Maps property name IDs to values on nodes
# Used by Schema__Semantic_Graph__Node for property storage
# Values are stored as Safe_Str__Text - consumer validates per property_type_id
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id        import Property_Name_Id
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict


class Dict__Node_Properties(Type_Safe__Dict):                                        # Maps property name IDs to values
    expected_key_type   = Property_Name_Id
    expected_value_type = Safe_Str__Text
