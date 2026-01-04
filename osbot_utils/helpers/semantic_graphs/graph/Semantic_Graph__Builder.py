# ═══════════════════════════════════════════════════════════════════════════════
# Semantic_Graph__Builder - Fluent builder for semantic graphs
# Provides convenient API for constructing graphs with proper ID management
#
# Updated for Brief 3.7:
#   - Nodes use node_type_id (can resolve from ref via registry)
#   - Edges use from_node_id, to_node_id, predicate_id (can resolve from ref)
#   - No line_number field
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Registry                   import Ontology__Registry
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id         import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph          import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge    import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node    import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.enum.Enum__Id__Source_Type            import Enum__Id__Source_Type
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id               import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref              import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id               import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref              import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Schema__Id__Source         import Schema__Id__Source
from osbot_utils.type_safe.Type_Safe                                                   import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                      import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                     import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                      import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                       import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id        import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed  import Safe_Str__Id__Seed
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                         import type_safe


class Semantic_Graph__Builder(Type_Safe):                                              # Fluent builder for semantic graphs
    graph             : Schema__Semantic_Graph                                         # Graph being built
    ontology_registry : Ontology__Registry      = None                                 # Optional: for resolving refs → IDs

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.graph:
            self.graph = Schema__Semantic_Graph(graph_id    = Graph_Id()                    ,
                                                ontology_id = Ontology_Id()                 ,
                                                nodes       = Dict__Nodes__By_Id()          ,
                                                edges       = List__Semantic_Graph__Edges() )

    # ═══════════════════════════════════════════════════════════════════════════
    # Graph configuration
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def with_ontology_id(self, ontology_id: Ontology_Id) -> 'Semantic_Graph__Builder':  # Set ontology ID
        self.graph.ontology_id = ontology_id
        return self

    @type_safe
    def with_registry(self, registry: Ontology__Registry) -> 'Semantic_Graph__Builder':  # Set registry for ref resolution
        self.ontology_registry = registry
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
    # Node operations (ID-based)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def add_node(self                               ,
                 node_type_id : Node_Type_Id        ,
                 name         : Safe_Str__Id        ,
                 node_id      : Node_Id        = None,
                 node_source  : Schema__Id__Source = None) -> 'Semantic_Graph__Builder':  # Add node with ID
        if node_id is None or node_id == '':
            node_id = Node_Id(Obj_Id())
        node = Schema__Semantic_Graph__Node(node_id        = node_id       ,
                                            node_id_source = node_source   ,
                                            node_type_id   = node_type_id  ,
                                            name           = name          )
        self.graph.nodes[node_id] = node
        return self

    @type_safe
    def add_node_by_ref(self                            ,
                        node_type_ref : Node_Type_Ref   ,
                        name          : Safe_Str__Id    ,
                        node_id       : Node_Id    = None,
                        node_source   : Schema__Id__Source = None) -> 'Semantic_Graph__Builder':
        if self.ontology_registry is None:                                             # Add node, resolving type ref → ID
            raise ValueError("Registry required to resolve node_type_ref to node_type_id")
        node_type_id = self.ontology_registry.get_node_type_id_by_ref(self.graph.ontology_id,
                                                                       node_type_ref)
        if node_type_id is None:
            raise ValueError(f"Unknown node type ref: {node_type_ref}")
        return self.add_node(node_type_id = node_type_id,
                             name         = name        ,
                             node_id      = node_id     ,
                             node_source  = node_source )

    @type_safe
    def add_node_with_seed(self                        ,
                           node_type_id : Node_Type_Id ,
                           name         : Safe_Str__Id ,
                           seed         : Safe_Str__Id__Seed) -> 'Semantic_Graph__Builder':  # Add node with deterministic ID
        node_id     = Node_Id(Obj_Id.from_seed(seed))
        node_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                         seed        = seed                               )
        return self.add_node(node_type_id = node_type_id,
                             name         = name        ,
                             node_id      = node_id     ,
                             node_source  = node_source )

    @type_safe
    def add_node_by_ref_with_seed(self                        ,
                                  node_type_ref : Node_Type_Ref,
                                  name          : Safe_Str__Id ,
                                  seed          : Safe_Str__Id__Seed) -> 'Semantic_Graph__Builder':
        if self.ontology_registry is None:                                             # Add node with seed, resolving ref
            raise ValueError("Registry required to resolve node_type_ref to node_type_id")
        node_type_id = self.ontology_registry.get_node_type_id_by_ref(self.graph.ontology_id,
                                                                       node_type_ref)
        if node_type_id is None:
            raise ValueError(f"Unknown node type ref: {node_type_ref}")
        return self.add_node_with_seed(node_type_id = node_type_id,
                                       name         = name        ,
                                       seed         = seed        )

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge operations (ID-based)
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def add_edge(self                                ,
                 from_node_id : Node_Id              ,
                 predicate_id : Predicate_Id         ,
                 to_node_id   : Node_Id              ,
                 edge_id      : Edge_Id         = None,
                 edge_source  : Schema__Id__Source = None) -> 'Semantic_Graph__Builder':  # Add edge with IDs
        if edge_id is None or edge_id == '':
            edge_id = Edge_Id(Obj_Id())
        edge = Schema__Semantic_Graph__Edge(edge_id        = edge_id      ,
                                            edge_id_source = edge_source  ,
                                            from_node_id   = from_node_id ,
                                            to_node_id     = to_node_id   ,
                                            predicate_id   = predicate_id )
        self.graph.edges.append(edge)
        return self

    @type_safe
    def add_edge_by_ref(self                             ,
                        from_node_id  : Node_Id          ,
                        predicate_ref : Predicate_Ref    ,
                        to_node_id    : Node_Id          ,
                        edge_id       : Edge_Id     = None,
                        edge_source   : Schema__Id__Source = None) -> 'Semantic_Graph__Builder':
        if self.ontology_registry is None:                                             # Add edge, resolving predicate ref → ID
            raise ValueError("Registry required to resolve predicate_ref to predicate_id")
        predicate_id = self.ontology_registry.get_predicate_id_by_ref(self.graph.ontology_id,
                                                                       predicate_ref)
        if predicate_id is None:
            raise ValueError(f"Unknown predicate ref: {predicate_ref}")
        return self.add_edge(from_node_id = from_node_id,
                             predicate_id = predicate_id,
                             to_node_id   = to_node_id  ,
                             edge_id      = edge_id     ,
                             edge_source  = edge_source )

    @type_safe
    def add_edge_with_seed(self                         ,
                           from_node_id : Node_Id       ,
                           predicate_id : Predicate_Id  ,
                           to_node_id   : Node_Id       ,
                           seed         : Safe_Str__Id__Seed) -> 'Semantic_Graph__Builder':  # Add edge with deterministic ID
        edge_id     = Edge_Id(Obj_Id.from_seed(seed))
        edge_source = Schema__Id__Source(source_type = Enum__Id__Source_Type.DETERMINISTIC,
                                         seed        = seed                               )
        return self.add_edge(from_node_id = from_node_id,
                             predicate_id = predicate_id,
                             to_node_id   = to_node_id  ,
                             edge_id      = edge_id     ,
                             edge_source  = edge_source )

    @type_safe
    def add_edge_by_ref_with_seed(self                         ,
                                  from_node_id  : Node_Id      ,
                                  predicate_ref : Predicate_Ref,
                                  to_node_id    : Node_Id      ,
                                  seed          : Safe_Str__Id__Seed) -> 'Semantic_Graph__Builder':
        if self.ontology_registry is None:                                             # Add edge with seed, resolving ref
            raise ValueError("Registry required to resolve predicate_ref to predicate_id")
        predicate_id = self.ontology_registry.get_predicate_id_by_ref(self.graph.ontology_id,
                                                                       predicate_ref)
        if predicate_id is None:
            raise ValueError(f"Unknown predicate ref: {predicate_ref}")
        return self.add_edge_with_seed(from_node_id = from_node_id,
                                       predicate_id = predicate_id,
                                       to_node_id   = to_node_id  ,
                                       seed         = seed        )

    # ═══════════════════════════════════════════════════════════════════════════
    # Build
    # ═══════════════════════════════════════════════════════════════════════════

    @type_safe
    def build(self) -> Schema__Semantic_Graph:                                         # Return completed graph
        return self.graph
