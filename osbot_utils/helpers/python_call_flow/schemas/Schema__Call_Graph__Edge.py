from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type  import Enum__Call_Graph__Edge_Type
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                    import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt


class Schema__Call_Graph__Edge(Type_Safe):                                           # Edge representing a relationship in call graph
    edge_id       : Edge_Id                                                          # Unique edge identifier
    from_node     : Node_Id                                                          # Source node_id
    to_node       : Node_Id                                                          # Target node_id
    edge_type     : Enum__Call_Graph__Edge_Type                                      # CONTAINS, CALLS, SELF, CHAIN
    line_number   : Safe_UInt                                                        # Line where relationship defined
    is_conditional: bool                         = False                             # Inside if/try/etc
