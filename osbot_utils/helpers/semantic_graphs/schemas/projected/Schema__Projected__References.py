# ═══════════════════════════════════════════════════════════════════════════════
# Schema__Projected__References - Lookup index from refs to IDs
#
# Updated for Brief 3.8:
#   - Added categories: Category refs used in the projection
#   - Added property_names: Property name refs used in the projection
#   - Added property_types: Property type refs used in the projection
#   - All fields now contain ONLY refs actually used in the projection (filtered)
#
# Maps TYPE refs (not instance names) to their IDs for tooling that needs
# to correlate back to Schema__ data.
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Category_Ids__By_Ref      import Dict__Category_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Type_Ids__By_Ref     import Dict__Node_Type_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicate_Ids__By_Ref     import Dict__Predicate_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Name_Ids__By_Ref import Dict__Property_Name_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Property_Type_Ids__By_Ref import Dict__Property_Type_Ids__By_Ref
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe


class Schema__Projected__References(Type_Safe):                                      # Ref → ID lookup index (filtered)
    node_types     : Dict__Node_Type_Ids__By_Ref                                     # Only types in graph nodes
    predicates     : Dict__Predicate_Ids__By_Ref                                     # Only predicates in graph edges
    categories     : Dict__Category_Ids__By_Ref                                      # Only categories of node types in graph
    property_names : Dict__Property_Name_Ids__By_Ref                                 # Only properties used in graph
    property_types : Dict__Property_Type_Ids__By_Ref                                 # Only types of used properties
