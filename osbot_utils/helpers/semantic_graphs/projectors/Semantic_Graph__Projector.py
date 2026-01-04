# ═══════════════════════════════════════════════════════════════════════════════
# Semantic_Graph__Projector - Transforms Schema__ to Projected__
#
# One-way transformation that generates human-readable projections from
# ID-based Schema__ data. The projection is generated, not edited.
#
# Requires access to Ontology__Registry to resolve IDs to refs.
# ═══════════════════════════════════════════════════════════════════════════════

from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Registry                 import Ontology__Registry
from osbot_utils.helpers.semantic_graphs.projected.Dict__Node_Type_Ids__By_Ref       import Dict__Node_Type_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.projected.Dict__Predicate_Ids__By_Ref       import Dict__Predicate_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.projected.List__Projected__Edges            import List__Projected__Edges
from osbot_utils.helpers.semantic_graphs.projected.List__Projected__Nodes            import List__Projected__Nodes
from osbot_utils.helpers.semantic_graphs.projected.Projected__Data                   import Projected__Data
from osbot_utils.helpers.semantic_graphs.projected.Projected__Edge                   import Projected__Edge
from osbot_utils.helpers.semantic_graphs.projected.Projected__Node                   import Projected__Node
from osbot_utils.helpers.semantic_graphs.projected.Projected__References             import Projected__References
from osbot_utils.helpers.semantic_graphs.projected.Projected__Semantic_Graph         import Projected__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.projected.Projected__Sources                import Projected__Sources
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph        import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref            import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref            import Predicate_Ref
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id      import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed import Safe_Str__Id__Seed
from osbot_utils.type_safe.primitives.domains.identifiers.Timestamp_Now              import Timestamp_Now
from osbot_utils.type_safe.type_safe_core.decorators.type_safe                       import type_safe


class Semantic_Graph__Projector(Type_Safe):                                          # Schema__ → Projected__ transformer
    ontology_registry : Ontology__Registry                                           # For resolving IDs to refs

    @type_safe
    def project(self, graph: Schema__Semantic_Graph) -> Projected__Semantic_Graph:   # Generate projection from schema
        ontology           = self.ontology_registry.get_by_id(graph.ontology_id)     # Get ontology for lookups
        node_type_id_to_ref = self.build_node_type_id_to_ref(ontology)               # Build reverse lookups
        predicate_id_to_ref = self.build_predicate_id_to_ref(ontology)
        node_id_to_name     = self.build_node_id_to_name(graph)                      # Build name lookup

        projected_nodes = self.project_nodes(graph, node_type_id_to_ref)             # Project nodes
        projected_edges = self.project_edges(graph, node_id_to_name, predicate_id_to_ref)  # Project edges
        references      = self.build_references(node_type_id_to_ref, predicate_id_to_ref)  # Build ref→ID index
        sources         = self.build_sources(graph, ontology)                        # Build provenance

        return Projected__Semantic_Graph(projection = Projected__Data(nodes = projected_nodes,
                                                                      edges = projected_edges),
                                         references = references                              ,
                                         sources    = sources                                 )

    # ═══════════════════════════════════════════════════════════════════════════
    # Reverse Lookup Builders
    # ═══════════════════════════════════════════════════════════════════════════

    def build_node_type_id_to_ref(self, ontology) -> dict:                           # Build ID → Ref map for node types
        if ontology is None:
            return {}
        return {nt.node_type_id: nt.node_type_ref for nt in ontology.node_types.values()}

    def build_predicate_id_to_ref(self, ontology) -> dict:                           # Build ID → Ref map for predicates
        if ontology is None:
            return {}
        return {p.predicate_id: p.predicate_ref for p in ontology.predicates.values()}

    def build_node_id_to_name(self, graph: Schema__Semantic_Graph) -> dict:          # Build Node_Id → name map
        return {node.node_id: node.name for node in graph.nodes.values()}

    # ═══════════════════════════════════════════════════════════════════════════
    # Projection Methods
    # ═══════════════════════════════════════════════════════════════════════════

    def project_nodes(self                   ,
                      graph                  : Schema__Semantic_Graph,
                      node_type_id_to_ref    : dict                  ) -> List__Projected__Nodes:
        result = List__Projected__Nodes()
        for node in graph.nodes.values():
            ref = node_type_id_to_ref.get(node.node_type_id, Node_Type_Ref(''))
            result.append(Projected__Node(ref  = ref      ,
                                          name = node.name))
        return result

    def project_edges(self                   ,
                      graph                  : Schema__Semantic_Graph,
                      node_id_to_name        : dict                  ,
                      predicate_id_to_ref    : dict                  ) -> List__Projected__Edges:
        result = List__Projected__Edges()
        for edge in graph.edges:
            from_name = node_id_to_name.get(edge.from_node_id, Safe_Str__Id(''))
            to_name   = node_id_to_name.get(edge.to_node_id  , Safe_Str__Id(''))
            ref       = predicate_id_to_ref.get(edge.predicate_id, Predicate_Ref(''))
            result.append(Projected__Edge(from_name = from_name,
                                          to_name   = to_name  ,
                                          ref       = ref      ))
        return result

    # ═══════════════════════════════════════════════════════════════════════════
    # References & Sources Builders
    # ═══════════════════════════════════════════════════════════════════════════

    def build_references(self                ,
                         node_type_id_to_ref : dict,
                         predicate_id_to_ref : dict) -> Projected__References:
        nodes_dict = Dict__Node_Type_Ids__By_Ref()                                   # Build ref → ID for node types
        for id, ref in node_type_id_to_ref.items():
            nodes_dict[ref] = id

        edges_dict = Dict__Predicate_Ids__By_Ref()                                   # Build ref → ID for predicates
        for id, ref in predicate_id_to_ref.items():
            edges_dict[ref] = id

        return Projected__References(nodes = nodes_dict,
                                     edges = edges_dict)

    def build_sources(self, graph: Schema__Semantic_Graph, ontology) -> Projected__Sources:
        ontology_seed = None                                                         # Get ontology seed if available
        if ontology and ontology.ontology_id_source:
            ontology_seed = ontology.ontology_id_source.seed

        return Projected__Sources(source_graph_id = graph.graph_id  ,
                                  ontology_seed   = ontology_seed   ,
                                  generated_at    = Timestamp_Now() )
