from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Id                 import Rule_Set_Id
from osbot_utils.helpers.semantic_graphs.schemas.ontology.Schema__Ontology              import Schema__Ontology
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb      import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                      import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                       import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                       import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                 import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph           import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node     import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge     import Schema__Semantic_Graph__Edge
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id         import Safe_Str__Id
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                          import type_safe


class Semantic_Graph__Builder(Type_Safe):                                            # Fluent API for building graphs
    graph    : Schema__Semantic_Graph                                                # The graph being built
    ontology : Schema__Ontology                                                      # Optional ontology for validation

    def create(self,
               ontology_id: Ontology_Id,                                               # Start building a new graph
               rule_set_id: Rule_Set_Id = None) -> 'Semantic_Graph__Builder':
        self.graph = Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id())       ,
                                            ontology_ref = Ontology_Id(ontology_id) ,
                                            rule_set_ref = Rule_Set_Id(rule_set_id) )
        return self

    def with_ontology(self, ontology: Schema__Ontology) -> 'Semantic_Graph__Builder':  # Set ontology for validation
        self.ontology = ontology
        return self

    @type_safe
    def add_node(self,
                 node_type  : Node_Type_Id,
                 name       : Safe_Str__Id,                                    # Add a node to the graph
                 line_number: int = 0) -> Node_Id:
        node_id = Node_Id(Obj_Id())
        node = Schema__Semantic_Graph__Node(
            node_id     = node_id                                                    ,
            node_type   = Node_Type_Id(node_type)                                    ,
            name        = name                                                       ,
            line_number = line_number                                                ,
        )
        self.graph.add_node(node)
        return node_id

    def add_edge(self,
                 from_node: Node_Id,
                 verb: Safe_Str__Ontology__Verb,
                 to_node: Node_Id,                                                  # Add an edge to the graph
                 line_number: int = 0
            ) -> Edge_Id:
        if self.ontology:                                                            # Validate if ontology available
            from_type = self.graph.get_node(from_node).node_type
            to_type   = self.graph.get_node(to_node).node_type
            if not self.ontology.valid_edge(from_type, verb, to_type):
                return None                                                          # returns None if valid_edge fails

        edge_id = Edge_Id(Obj_Id())
        edge = Schema__Semantic_Graph__Edge(
            edge_id     = edge_id                                                    ,
            from_node   = from_node                                                  ,
            verb        = Safe_Str__Ontology__Verb(verb)                             ,
            to_node     = to_node                                                    ,
            line_number = line_number                                                ,
        )
        self.graph.add_edge(edge)
        return edge_id

    def build(self) -> Schema__Semantic_Graph:                                       # Return the completed graph
        return self.graph

    def find_node_by_name(self, name: Safe_Str__Id) -> Node_Id:                     # Find node by name
        for node in self.graph.nodes.values():
            if node.name == name:
                return node.node_id
        return None

    # todo: convert to type_safe list
    def find_nodes_by_type(self, node_type: Schema__Semantic_Graph__Node) -> list:                            # Find all nodes of type
        return [n.node_id for n in self.graph.nodes.values() if n.node_type == node_type]
