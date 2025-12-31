# osbot_utils/helpers/ast/call_flow/schemas/Schema__Call_Graph.py

from typing                                                                          import Dict, List
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Config         import Schema__Call_Graph__Config
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Edge           import Schema__Call_Graph__Edge
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Node           import Schema__Call_Graph__Node
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                   import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label   import Safe_Str__Label
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt



class Schema__Call_Graph(Type_Safe):                                                 # Complete call graph structure
    graph_id        : Graph_Id                                                       # Unique graph identifier
    name            : Safe_Str__Label                                                # Descriptive name for the graph
    entry_point     : Node_Id                                                        # Starting node_id
    config          : Schema__Call_Graph__Config                                     # Configuration used
    nodes           : Dict[str, Schema__Call_Graph__Node]                            # node_id -> node
    edges           : List[Schema__Call_Graph__Edge]                                 # All edges
    max_depth_found : Safe_UInt                 = Safe_UInt(0)                       # Deepest level reached

    # todo: refactor out all these methods (since schemas should not have code)
    def add_node(self, node: Schema__Call_Graph__Node) -> 'Schema__Call_Graph':      # Add node to graph
        node_id = str(node.node_id)
        self.nodes[node_id] = node
        return self

    def add_edge(self, edge: Schema__Call_Graph__Edge) -> 'Schema__Call_Graph':      # Add edge to graph
        self.edges.append(edge)
        return self

    def get_node(self, node_id: str) -> Schema__Call_Graph__Node:                    # Get node by id
        return self.nodes.get(node_id)

    def node_count(self) -> int:                                                     # Total nodes
        return len(self.nodes)

    def edge_count(self) -> int:                                                     # Total edges
        return len(self.edges)

    def leaf_nodes(self) -> List[Schema__Call_Graph__Node]:                          # Nodes with no outgoing calls
        leaves = []
        for node in self.nodes.values():
            if not node.calls:
                leaves.append(node)
        return leaves

    def root_nodes(self) -> List[Schema__Call_Graph__Node]:                          # Nodes with no incoming calls
        roots = []
        for node in self.nodes.values():
            if not node.called_by:
                roots.append(node)
        return roots

    def nodes_at_depth(self, depth: int) -> List[Schema__Call_Graph__Node]:          # Get all nodes at specific depth
        return [n for n in self.nodes.values() if int(n.depth) == depth]