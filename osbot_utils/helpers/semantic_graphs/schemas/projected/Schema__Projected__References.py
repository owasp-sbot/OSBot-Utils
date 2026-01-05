# ═══════════════════════════════════════════════════════════════════════════════
# Projected__References - Lookup index from refs to IDs
#
# Maps TYPE refs (not instance names) to their IDs for tooling that needs
# to correlate back to Schema__ data.
#
# Example:
#   nodes: {"class": "9e8d7c6b", "method": "1a2b3c4d"}
#   edges: {"calls": "p1p2p3p4", "contains": "p5p6p7p8"}
# ═══════════════════════════════════════════════════════════════════════════════
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Type_Ids__By_Ref import Dict__Node_Type_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicate_Ids__By_Ref import Dict__Predicate_Ids__By_Ref
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe


class Schema__Projected__References(Type_Safe):                                              # Ref → ID lookup index
    nodes : Dict__Node_Type_Ids__By_Ref                                              # Node type ref → ID
    edges : Dict__Predicate_Ids__By_Ref                                              # Predicate ref → ID
