# ═══════════════════════════════════════════════════════════════════════════════
# Semantic_Graph__Builder - Fluent builder for semantic graphs
# Provides convenient API for constructing graphs with proper ID management
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id         import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph          import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge    import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node    import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type            import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref              import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref               import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref               import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source         import Schema__Id__Source
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb     import Safe_Str__Ontology__Verb
from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                   import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version        import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                      import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                     import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                      import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                       import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id        import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed  import Safe_Str__Id__Seed
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                         import type_safe


class Semantic_Graph__Builder(Type_Safe):                                              # Fluent builder for semantic graphs
    graph : Schema__Semantic_Graph                                                     # Graph being built

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.graph:
            self.graph = Schema__Semantic_Graph(graph_id     = Graph_Id()             ,
                                                ontology_ref = Ontology_Ref()         ,
                                                rule_set_ref = Rule_Set_Ref()         ,
                                                nodes        = Dict__Nodes__By_Id()   ,
                                                edges        = List__Semantic_Graph__Edges())

    # ═══════════════════════════════════════════════════════════════════════════
    # Graph configuration
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def with_ontology(self, ontology_ref: Ontology_Ref) -> 'Semantic_Graph__Builder':  # Set ontology ref
        self.graph.ontology_ref = ontology_ref
        return self

    @type_safe
    def with_rule_set(self, rule_set_ref: Rule_Set_Ref) -> 'Semantic_Graph__Builder':  # Set rule set ref
        self.graph.rule_set_ref = rule_set_ref
        return self

    @type_safe
    def with_version(self, version: Safe_Str__Version) -> 'Semantic_Graph__Builder':   # Set version
        self.graph.version = version
        return self

    @type_safe
    def with_graph_id(self                          ,
                      graph_id : Graph_Id           ,
                      source   : Schema__Id__Source = None) -> 'Semantic_Graph__Builder':  # Set graph ID
        self.graph.graph_id        = graph_id
        self.graph.graph_id_source = source
        return self

    @type_safe
    def with_deterministic_graph_id(self              ,
                                    seed: Safe_Str__Id__Seed) -> 'Semantic_Graph__Builder':  # Set deterministic graph ID
        self.graph.graph_id        = Graph_Id(Obj_Id.from_seed(seed))
        self.graph.graph_id_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                                        seed        = seed                                )
        return self

    # ═══════════════════════════════════════════════════════════════════════════
    # Node operations
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def add_node(self                               ,
                 node_type   : Node_Type_Ref        ,
                 name        : Safe_Str__Id         ,
                 node_id     : Node_Id              = None,
                 node_source : Schema__Id__Source   = None,
                 line_number : Safe_UInt            = None) -> 'Semantic_Graph__Builder':  # Add node
        if node_id is None or node_id == '':
            node_id = Node_Id(Obj_Id())
        node = Schema__Semantic_Graph__Node(node_id        = node_id                ,
                                            node_id_source = node_source            ,
                                            node_type      = node_type              ,
                                            name           = name                   ,
                                            line_number    = line_number or Safe_UInt(0))
        self.graph.nodes[node_id] = node
        return self

    @type_safe
    def add_node_with_seed(self                        ,
                           node_type   : Node_Type_Ref ,
                           name        : Safe_Str__Id  ,
                           seed        : Safe_Str__Id__Seed,
                           line_number : Safe_UInt     = None) -> 'Semantic_Graph__Builder':  # Add node with deterministic ID
        node_id     = Node_Id(Obj_Id.from_seed(seed))
        node_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                         seed        = seed                               )
        return self.add_node(node_type   = node_type   ,
                             name        = name        ,
                             node_id     = node_id     ,
                             node_source = node_source ,
                             line_number = line_number )

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge operations
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def add_edge(self                                ,
                 from_node   : Node_Id               ,
                 verb        : Safe_Str__Ontology__Verb,
                 to_node     : Node_Id               ,
                 edge_id     : Edge_Id               = None,
                 edge_source : Schema__Id__Source    = None,
                 line_number : Safe_UInt             = None) -> 'Semantic_Graph__Builder':  # Add edge
        if edge_id is None or edge_id == '':
            edge_id = Edge_Id(Obj_Id())
        edge = Schema__Semantic_Graph__Edge(edge_id        = edge_id                ,
                                            edge_id_source = edge_source            ,
                                            from_node      = from_node              ,
                                            verb           = verb                   ,
                                            to_node        = to_node                ,
                                            line_number    = line_number or Safe_UInt(0))
        self.graph.edges.append(edge)
        return self

    @type_safe
    def add_edge_with_seed(self                         ,
                           from_node   : Node_Id        ,
                           verb        : Safe_Str__Ontology__Verb,
                           to_node     : Node_Id        ,
                           seed        : Safe_Str__Id__Seed,
                           line_number : Safe_UInt      = None) -> 'Semantic_Graph__Builder':  # Add edge with deterministic ID
        edge_id     = Edge_Id(Obj_Id.from_seed(seed))
        edge_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                         seed        = seed                               )
        return self.add_edge(from_node   = from_node   ,
                             verb        = verb        ,
                             to_node     = to_node     ,
                             edge_id     = edge_id     ,
                             edge_source = edge_source ,
                             line_number = line_number )

    # ═══════════════════════════════════════════════════════════════════════════
    # Build
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def build(self) -> Schema__Semantic_Graph:                                         # Return completed graph
        return self.graph
