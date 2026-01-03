from typing                                                                          import Dict, List
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id              import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version      import Safe_Str__Version
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge  import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node  import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id              import Ontology_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                   import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id

# refactor out methods

class Schema__Semantic_Graph(Type_Safe):                                             # Complete semantic graph instance
    graph_id     : Graph_Id                                                          # Unique identifier
    version      : Safe_Str__Version             = Safe_Str__Version('1.0.0')        # Graph version
    ontology_ref : Ontology_Id                                                       # Which ontology defines types
    rule_set_ref : Rule_Set_Id                                                       # Optional rule set
    nodes        : Dict[Node_Id, Schema__Semantic_Graph__Node]                       # node_id → node
    edges        : List[Schema__Semantic_Graph__Edge]                                # All edges

    def add_node(self, node: Schema__Semantic_Graph__Node) -> 'Schema__Semantic_Graph':
        self.nodes[node.node_id] = node
        return self

    def add_edge(self, edge: Schema__Semantic_Graph__Edge) -> 'Schema__Semantic_Graph':
        self.edges.append(edge)
        return self

    def get_node(self, node_id: Node_Id) -> Schema__Semantic_Graph__Node:                # Get node by ID
        return self.nodes.get(node_id)

    def node_count(self) -> int:                                                     # Total nodes
        return len(self.nodes)

    def edge_count(self) -> int:                                                     # Total edges
        return len(self.edges)

    def nodes_by_type(self, node_type: Node_Type_Id) -> List[Schema__Semantic_Graph__Node]:   # Get all nodes of a type
        return [n for n in self.nodes.values() if n.node_type == node_type]

    def edges_from(self, node_id: Node_Id) -> List[Schema__Semantic_Graph__Edge]:        # Get outgoing edges
        return [e for e in self.edges if e.from_node == node_id]

    def edges_to(self, node_id: Node_Id) -> List[Schema__Semantic_Graph__Edge]:          # Get incoming edges
        return [e for e in self.edges if e.to_node == node_id]

    def edges_by_verb(self, verb: Safe_Str__Ontology__Verb) -> List[Schema__Semantic_Graph__Edge]:        # Get edges by verb
        return [e for e in self.edges if e.verb == verb]

    def neighbors(self, node_id: Node_Id,
                  verb: Safe_Str__Ontology__Verb = None
             ) -> List[Node_Id]:                # Get connected node IDs
        result = []
        for edge in self.edges_from(node_id):
            if verb is None or edge.verb == verb:
                result.append(edge.to_node)
        return result

    def reverse_neighbors(self, node_id: Node_Id,
                          verb: Safe_Str__Ontology__Verb = None
                     ) -> List[Node_Id]:        # Get nodes pointing to this one
        result = []
        for edge in self.edges_to(node_id):
            if verb is None or edge.verb == verb:
                result.append(edge.from_node)
        return result
