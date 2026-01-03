# ═══════════════════════════════════════════════════════════════════════════════
# Semantic_Graph__Builder - Fluent API for building graphs
# Refactored to use Semantic_Graph__Utils for graph operations
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id              import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology           import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph        import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node  import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge  import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id              import Ontology_Id
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Utils                 import Semantic_Graph__Utils
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Utils                    import Ontology__Utils
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                 import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                   import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                    import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id      import Safe_Str__Id
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                       import type_safe


class Semantic_Graph__Builder(Type_Safe):                                            # Fluent API for building graphs
    graph          : Schema__Semantic_Graph                                          # The graph being built
    ontology       : Schema__Ontology                                                # Optional ontology for validation
    graph_utils    : Semantic_Graph__Utils                                           # Graph operations helper
    ontology_utils : Ontology__Utils                                                 # Ontology operations helper

    def create(self, ontology_id: Ontology_Id,                                       # Start building a new graph
                     rule_set_id: Rule_Set_Id = None) -> 'Semantic_Graph__Builder':
        self.graph = Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                            ontology_ref = Ontology_Id(ontology_id),
                                            rule_set_ref = Rule_Set_Id(rule_set_id))
        return self

    def with_ontology(self, ontology: Schema__Ontology) -> 'Semantic_Graph__Builder':  # Set ontology for validation
        self.ontology = ontology
        return self

    @type_safe
    def add_node(self, node_type  : Node_Type_Id,
                       name       : Safe_Str__Id,                                    # Add a node to the graph
                       line_number: Safe_UInt = 0) -> Node_Id:
        node_id = Node_Id(Obj_Id())
        node = Schema__Semantic_Graph__Node(node_id     = node_id                ,
                                            node_type   = Node_Type_Id(node_type),
                                            name        = name                   ,
                                            line_number = line_number            )
        self.graph_utils.add_node(self.graph, node)
        return node_id

    @type_safe
    def add_edge(self, from_node  : Node_Id                ,
                       verb       : Safe_Str__Ontology__Verb,
                       to_node    : Node_Id                ,                         # Add an edge to the graph
                       line_number: Safe_UInt = 0          ) -> Edge_Id:
        if self.ontology:                                                            # Validate if ontology available
            from_node_obj = self.graph_utils.get_node(self.graph, from_node)
            to_node_obj   = self.graph_utils.get_node(self.graph, to_node)
            from_type     = from_node_obj.node_type
            to_type       = to_node_obj.node_type
            if self.ontology_utils.valid_edge(self.ontology, from_type, verb, to_type) is False:
                return None                                                          # Returns None if valid_edge fails

        edge_id = Edge_Id(Obj_Id())
        edge = Schema__Semantic_Graph__Edge(edge_id     = edge_id                          ,
                                            from_node   = from_node                        ,
                                            verb        = Safe_Str__Ontology__Verb(verb)   ,
                                            to_node     = to_node                          ,
                                            line_number = line_number                      )
        self.graph_utils.add_edge(self.graph, edge)
        return edge_id

    def build(self) -> Schema__Semantic_Graph:                                       # Return the completed graph
        return self.graph

    @type_safe
    def find_node_by_name(self, name: Safe_Str__Id) -> Node_Id:                     # Find node by name
        for node in self.graph.nodes.values():
            if node.name == name:
                return node.node_id
        return None

    @type_safe
    def find_nodes_by_type(self, node_type: Node_Type_Id) -> list:                  # Find all nodes of type
        return [n.node_id for n in self.graph.nodes.values() if n.node_type == node_type]