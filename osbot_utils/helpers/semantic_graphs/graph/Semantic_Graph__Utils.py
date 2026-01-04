# ═══════════════════════════════════════════════════════════════════════════════
# Semantic_Graph__Utils - Operations on Schema__Semantic_Graph (business logic)
# All operations take graph as first parameter - schemas remain pure data
#
# Updated for Brief 3.7:
#   - Nodes reference node_type_id (not node_type ref)
#   - Edges use from_node_id, to_node_id, predicate_id (not from_node, to_node, verb)
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Node_Ids             import List__Node_Ids
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph          import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge    import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node    import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id               import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id               import Predicate_Id
from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                      import Node_Id
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                         import type_safe


class Semantic_Graph__Utils(Type_Safe):                                                # Operations on semantic graph schemas

    @type_safe
    def get_node(self                      ,
                 graph   : Schema__Semantic_Graph,
                 node_id : Node_Id               ) -> Schema__Semantic_Graph__Node:    # Get node by ID
        return graph.nodes.get(node_id)

    @type_safe
    def has_node(self                      ,
                 graph   : Schema__Semantic_Graph,
                 node_id : Node_Id               ) -> bool:                            # Check if node exists
        return node_id in graph.nodes

    @type_safe
    def all_node_ids(self                  ,
                     graph : Schema__Semantic_Graph) -> List__Node_Ids:                # All node IDs
        result = List__Node_Ids()
        for node_id in graph.nodes.keys():
            result.append(node_id)
        return result

    @type_safe
    def node_count(self                    ,
                   graph : Schema__Semantic_Graph) -> int:                             # Number of nodes
        return len(graph.nodes)

    @type_safe
    def edge_count(self                    ,
                   graph : Schema__Semantic_Graph) -> int:                             # Number of edges
        return len(graph.edges)

    @type_safe
    def nodes_by_type(self                       ,
                      graph        : Schema__Semantic_Graph,
                      node_type_id : Node_Type_Id          ) -> List__Node_Ids:        # Nodes of specific type
        result = List__Node_Ids()
        for node_id, node in graph.nodes.items():
            if node.node_type_id == node_type_id:
                result.append(node_id)
        return result

    @type_safe
    def outgoing_edges(self                ,
                       graph   : Schema__Semantic_Graph,
                       node_id : Node_Id               ) -> List__Semantic_Graph__Edges:  # Edges from node
        result = List__Semantic_Graph__Edges()
        for edge in graph.edges:
            if edge.from_node_id == node_id:
                result.append(edge)
        return result

    @type_safe
    def incoming_edges(self                ,
                       graph   : Schema__Semantic_Graph,
                       node_id : Node_Id               ) -> List__Semantic_Graph__Edges:  # Edges to node
        result = List__Semantic_Graph__Edges()
        for edge in graph.edges:
            if edge.to_node_id == node_id:
                result.append(edge)
        return result

    @type_safe
    def edges_with_predicate(self                    ,
                             graph        : Schema__Semantic_Graph,
                             predicate_id : Predicate_Id          ) -> List__Semantic_Graph__Edges:  # Edges with predicate
        result = List__Semantic_Graph__Edges()
        for edge in graph.edges:
            if edge.predicate_id == predicate_id:
                result.append(edge)
        return result

    @type_safe
    def neighbors(self                     ,
                  graph   : Schema__Semantic_Graph,
                  node_id : Node_Id               ) -> List__Node_Ids:                 # Adjacent nodes
        result = List__Node_Ids()
        for edge in graph.edges:
            if edge.from_node_id == node_id and edge.to_node_id not in result:
                result.append(edge.to_node_id)
            if edge.to_node_id == node_id and edge.from_node_id not in result:
                result.append(edge.from_node_id)
        return result

    @type_safe
    def has_edge(self                                ,
                 graph        : Schema__Semantic_Graph,
                 from_node_id : Node_Id               ,
                 predicate_id : Predicate_Id          ,
                 to_node_id   : Node_Id               ) -> bool:                       # Check if edge exists
        for edge in graph.edges:
            if (edge.from_node_id == from_node_id and
                edge.predicate_id == predicate_id and
                edge.to_node_id   == to_node_id):
                return True
        return False

    @type_safe
    def find_edge(self                               ,
                  graph        : Schema__Semantic_Graph,
                  from_node_id : Node_Id               ,
                  predicate_id : Predicate_Id          ,
                  to_node_id   : Node_Id               ) -> Schema__Semantic_Graph__Edge:  # Find specific edge
        for edge in graph.edges:
            if (edge.from_node_id == from_node_id and
                edge.predicate_id == predicate_id and
                edge.to_node_id   == to_node_id):
                return edge
        return None

    @type_safe
    def outgoing_neighbors(self                ,
                           graph   : Schema__Semantic_Graph,
                           node_id : Node_Id               ) -> List__Node_Ids:        # Nodes this node points to
        result = List__Node_Ids()
        for edge in graph.edges:
            if edge.from_node_id == node_id and edge.to_node_id not in result:
                result.append(edge.to_node_id)
        return result

    @type_safe
    def incoming_neighbors(self                ,
                           graph   : Schema__Semantic_Graph,
                           node_id : Node_Id               ) -> List__Node_Ids:        # Nodes pointing to this node
        result = List__Node_Ids()
        for edge in graph.edges:
            if edge.to_node_id == node_id and edge.from_node_id not in result:
                result.append(edge.from_node_id)
        return result
