# ═══════════════════════════════════════════════════════════════════════════════
# Semantic_Graph__Utils - Utility operations for semantic graphs
# Extracted from Schema__Semantic_Graph to keep schemas as pure data containers
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id            import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph       import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb  import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                   import Node_Id
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                      import type_safe


class Semantic_Graph__Utils(Type_Safe):                                              # Utility operations for semantic graphs

    # ═══════════════════════════════════════════════════════════════════════════════
    # Node Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def add_node(self, graph: Schema__Semantic_Graph,
                       node : Schema__Semantic_Graph__Node) -> Schema__Semantic_Graph:
        graph.nodes[node.node_id] = node                                             # Add node to graph's node dict
        return graph

    @type_safe
    def get_node(self, graph  : Schema__Semantic_Graph,
                       node_id: Node_Id               ) -> Schema__Semantic_Graph__Node:
        return graph.nodes.get(node_id)                                              # Get node by ID, None if not found

    @type_safe
    def node_count(self, graph: Schema__Semantic_Graph) -> int:                      # Total number of nodes
        return len(graph.nodes)

    @type_safe
    def nodes_by_type(self, graph    : Schema__Semantic_Graph,
                            node_type: Node_Type_Id          ) -> list:              # Get all nodes of a specific type
        return [n for n in graph.nodes.values() if n.node_type == node_type]

    # ═══════════════════════════════════════════════════════════════════════════════
    # Edge Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def add_edge(self, graph: Schema__Semantic_Graph,
                       edge : Schema__Semantic_Graph__Edge) -> Schema__Semantic_Graph:
        graph.edges.append(edge)                                                     # Add edge to graph's edge list
        return graph

    @type_safe
    def edge_count(self, graph: Schema__Semantic_Graph) -> int:                      # Total number of edges
        return len(graph.edges)

    @type_safe
    def edges_from(self, graph  : Schema__Semantic_Graph,
                         node_id: Node_Id               ) -> list:                   # Get outgoing edges from node
        return [e for e in graph.edges if e.from_node == node_id]

    @type_safe
    def edges_to(self, graph  : Schema__Semantic_Graph,
                       node_id: Node_Id               ) -> list:                     # Get incoming edges to node
        return [e for e in graph.edges if e.to_node == node_id]

    @type_safe
    def edges_by_verb(self, graph: Schema__Semantic_Graph,
                            verb : Safe_Str__Ontology__Verb) -> list:                # Get edges by relationship verb
        return [e for e in graph.edges if e.verb == verb]

    # ═══════════════════════════════════════════════════════════════════════════════
    # Neighbor Operations
    # ═══════════════════════════════════════════════════════════════════════════════

    @type_safe
    def neighbors(self, graph  : Schema__Semantic_Graph     ,
                        node_id: Node_Id                    ,
                        verb   : Safe_Str__Ontology__Verb = None) -> list:           # Get connected node IDs (outgoing)
        result = []
        for edge in self.edges_from(graph, node_id):
            if verb is None or edge.verb == verb:
                result.append(edge.to_node)
        return result

    @type_safe
    def reverse_neighbors(self, graph  : Schema__Semantic_Graph     ,
                                node_id: Node_Id                    ,
                                verb   : Safe_Str__Ontology__Verb = None) -> list:   # Get nodes pointing to this one
        result = []
        for edge in self.edges_to(graph, node_id):
            if verb is None or edge.verb == verb:
                result.append(edge.from_node)
        return result
