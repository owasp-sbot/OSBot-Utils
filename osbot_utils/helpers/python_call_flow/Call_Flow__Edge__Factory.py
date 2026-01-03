from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Edge          import Schema__Call_Graph__Edge
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type import Enum__Call_Graph__Edge_Type
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt


class Call_Flow__Edge__Factory(Type_Safe):                                           # Factory for creating Schema__Call_Graph__Edge instances

    def create(self, from_node: Node_Id, to_node: Node_Id,                           # Create an edge between two nodes
               edge_type: Enum__Call_Graph__Edge_Type,
               line_number: int = 0) -> Schema__Call_Graph__Edge:

        return Schema__Call_Graph__Edge(
            edge_id     = Edge_Id(Obj_Id())                                          ,
            from_node   = from_node                                                  ,
            to_node     = to_node                                                    ,
            edge_type   = edge_type                                                  ,
            line_number = Safe_UInt(line_number)                                     ,
        )

    def create_contains(self, from_node: Node_Id, to_node: Node_Id,                  # Create CONTAINS edge (class → method)
                        line_number: int = 0) -> Schema__Call_Graph__Edge:
        return self.create(from_node, to_node, Enum__Call_Graph__Edge_Type.CONTAINS, line_number)

    def create_calls(self, from_node: Node_Id, to_node: Node_Id,                     # Create CALLS edge (direct function call)
                     line_number: int = 0) -> Schema__Call_Graph__Edge:
        return self.create(from_node, to_node, Enum__Call_Graph__Edge_Type.CALLS, line_number)

    def create_self(self, from_node: Node_Id, to_node: Node_Id,                      # Create SELF edge (self.method() call)
                    line_number: int = 0) -> Schema__Call_Graph__Edge:
        return self.create(from_node, to_node, Enum__Call_Graph__Edge_Type.SELF, line_number)

    def create_chain(self, from_node: Node_Id, to_node: Node_Id,                     # Create CHAIN edge (obj.method() call)
                     line_number: int = 0) -> Schema__Call_Graph__Edge:
        return self.create(from_node, to_node, Enum__Call_Graph__Edge_Type.CHAIN, line_number)
