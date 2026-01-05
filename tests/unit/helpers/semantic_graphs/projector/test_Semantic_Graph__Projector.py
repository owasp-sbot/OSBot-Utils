# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic_Graph__Projector - Tests for Schema__ to Projected__ transformation
#
# Brief 3.8 Compliance:
#   - Four sections: projection, references, taxonomy, sources
#   - Properties projected with Property_Name_Ref keys
#   - References filtered to only what's used
#   - Taxonomy section with node_type_categories and category_parents
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                 import TestCase
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Registry                          import Ontology__Registry
from osbot_utils.helpers.semantic_graphs.projector.Semantic_Graph__Projector                  import Semantic_Graph__Projector
from osbot_utils.helpers.semantic_graphs.taxonomy.Taxonomy__Registry                          import Taxonomy__Registry
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Type_Ids__By_Ref       import Dict__Node_Type_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id                import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicate_Ids__By_Ref       import Dict__Predicate_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Projected_Properties        import Dict__Projected_Properties
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Projected__Edges            import List__Projected__Edges
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Projected__Nodes            import List__Projected__Nodes
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges       import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph                 import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Category_Ref                      import Category_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                      import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                     import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                       import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                      import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref                     import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Ref                 import Property_Name_Ref
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Data            import Schema__Projected__Data
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Edge            import Schema__Projected__Edge
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Node            import Schema__Projected__Node
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__References      import Schema__Projected__References
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Semantic_Graph  import Schema__Projected__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Sources         import Schema__Projected__Sources
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Taxonomy        import Schema__Projected__Taxonomy
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data               import QA__Semantic_Graphs__Test_Data
from osbot_utils.testing.__                                                                   import __, __SKIP__
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                            import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                              import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now              import Timestamp_Now
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id               import Safe_Str__Id


class test_Semantic_Graph__Projector(TestCase):                                              # Test projector transformation

    @classmethod
    def setUpClass(cls):                                                                     # Shared setup
        cls.test_data         = QA__Semantic_Graphs__Test_Data()
        cls.fixture           = cls.test_data.create_complete_fixture()                      # Brief 3.8 API
        cls.ontology_registry = cls.fixture['ontology_registry']
        cls.taxonomy_registry = cls.fixture['taxonomy_registry']
        cls.ontology          = cls.fixture['ontology']
        cls.taxonomy          = cls.fixture['taxonomy']
        cls.graph             = cls.fixture['graph']
        cls.projector         = cls.fixture['projector']

    def test__init__(self):                                                                  # Test basic initialization
        with Semantic_Graph__Projector() as _:
            assert type(_)                   is Semantic_Graph__Projector
            assert type(_.ontology_registry) is Ontology__Registry

    def test__init__with_registries(self):                                                   # Test initialization with registries
        ontology_registry = Ontology__Registry()
        taxonomy_registry = Taxonomy__Registry()
        projector = Semantic_Graph__Projector(ontology_registry = ontology_registry,
                                              taxonomy_registry = taxonomy_registry)

        assert projector.ontology_registry is ontology_registry
        assert projector.taxonomy_registry is taxonomy_registry

    # ═══════════════════════════════════════════════════════════════════════════
    # Main Project Method Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__project(self):                                                                 # Test main projection method
        projected = self.projector.project(self.graph)

        assert type(projected)            is Schema__Projected__Semantic_Graph
        assert type(projected.projection) is Schema__Projected__Data
        assert type(projected.references) is Schema__Projected__References
        assert type(projected.taxonomy)   is Schema__Projected__Taxonomy                     # Brief 3.8: new section
        assert type(projected.sources)    is Schema__Projected__Sources

    def test__project__returns_four_sections(self):                                          # Brief 3.8: exactly four sections
        projected = self.projector.project(self.graph)

        assert hasattr(projected, 'projection')                                              # Data section
        assert hasattr(projected, 'references')                                              # Lookups section
        assert hasattr(projected, 'taxonomy')                                                # Taxonomy section (Brief 3.8)
        assert hasattr(projected, 'sources')                                                 # Provenance section

    def test__project__projection_has_nodes_and_edges(self):                                 # Projection section structure
        projected = self.projector.project(self.graph)

        assert type(projected.projection.nodes) is List__Projected__Nodes
        assert type(projected.projection.edges) is List__Projected__Edges
        assert len(projected.projection.nodes)  == 4                                         # module, class, method, function
        assert len(projected.projection.edges)  == 4                                         # contains x3, calls x1

    def test__project__node_count_matches_graph(self):                                       # Projected nodes match source
        projected = self.projector.project(self.graph)

        assert len(projected.projection.nodes) == len(self.graph.nodes)

    def test__project__edge_count_matches_graph(self):                                       # Projected edges match source
        projected = self.projector.project(self.graph)

        assert len(projected.projection.edges) == len(self.graph.edges)

    # ═══════════════════════════════════════════════════════════════════════════
    # Brief 3.8 Compliance: Properties in Projection
    # ═══════════════════════════════════════════════════════════════════════════

    def test__project__nodes_have_properties(self):                                          # Brief 3.8: properties projected
        projected = self.projector.project(self.graph)

        nodes_with_props = [n for n in projected.projection.nodes if n.properties]
        assert len(nodes_with_props) >= 1                                                    # At least one has properties

    def test__project__node_properties_use_refs(self):                                       # Properties keyed by Property_Name_Ref
        projected = self.projector.project(self.graph)

        for node in projected.projection.nodes:
            if node.properties:
                assert type(node.properties) is Dict__Projected_Properties
                for key in node.properties.keys():
                    assert type(key) is Property_Name_Ref                                    # Refs, not IDs

    def test__project__edges_have_properties(self):                                          # Brief 3.8: edge properties projected
        projected = self.projector.project(self.graph)

        edges_with_props = [e for e in projected.projection.edges if e.properties]
        assert len(edges_with_props) >= 1                                                    # At least one has properties

    def test__project__edge_properties_use_refs(self):                                       # Properties keyed by Property_Name_Ref
        projected = self.projector.project(self.graph)

        for edge in projected.projection.edges:
            if edge.properties:
                assert type(edge.properties) is Dict__Projected_Properties
                for key in edge.properties.keys():
                    assert type(key) is Property_Name_Ref                                    # Refs, not IDs

    # ═══════════════════════════════════════════════════════════════════════════
    # Brief 3.8 Compliance: Filtered References
    # ═══════════════════════════════════════════════════════════════════════════

    def test__project__references_are_filtered(self):                                        # Only used refs included
        projected = self.projector.project(self.graph)

        used_node_types_in_graph = set()
        for node in self.graph.nodes.values():
            nt = self.ontology.node_types.get(node.node_type_id)
            if nt:
                used_node_types_in_graph.add(str(nt.node_type_ref))

        ref_node_types = set(str(r) for r in projected.references.node_types.keys())

        # All used types are in references
        for used in used_node_types_in_graph:
            assert used in ref_node_types

    def test__project__references_contain_used_predicates(self):                             # Only used predicates
        projected = self.projector.project(self.graph)

        used_predicates_in_graph = set()
        for edge in self.graph.edges:
            pred = self.ontology.predicates.get(edge.predicate_id)
            if pred:
                used_predicates_in_graph.add(str(pred.predicate_ref))

        ref_predicates = set(str(r) for r in projected.references.predicates.keys())

        for used in used_predicates_in_graph:
            assert used in ref_predicates

    # ═══════════════════════════════════════════════════════════════════════════
    # Brief 3.8 Compliance: Taxonomy Section
    # ═══════════════════════════════════════════════════════════════════════════

    def test__project__has_taxonomy_section(self):                                           # Brief 3.8: taxonomy section exists
        projected = self.projector.project(self.graph)

        assert type(projected.taxonomy) is Schema__Projected__Taxonomy
        assert projected.taxonomy.node_type_categories is not None
        assert projected.taxonomy.category_parents     is not None

    def test__project__taxonomy_maps_node_types_to_categories(self):                         # Node type → category mapping
        projected = self.projector.project(self.graph)

        for node_type_ref, category_ref in projected.taxonomy.node_type_categories.items():
            assert type(node_type_ref) is Node_Type_Ref
            assert type(category_ref)  is Category_Ref

    def test__project__taxonomy_preserves_hierarchy(self):                                   # Category parent links
        projected = self.projector.project(self.graph)

        for category_ref, parent_ref in projected.taxonomy.category_parents.items():
            assert type(category_ref) is Category_Ref
            # parent_ref can be Category_Ref or None for root

    # ═══════════════════════════════════════════════════════════════════════════
    # Brief 3.8 Compliance: No IDs in Projection
    # ═══════════════════════════════════════════════════════════════════════════

    def test__project__projection_contains_no_ids(self):                                     # Key requirement
        projected = self.projector.project(self.graph)

        json_str = projected.projection.json()
        json_text = str(json_str)

        assert 'node_id'      not in json_text                                               # No instance IDs
        assert 'edge_id'      not in json_text
        assert 'node_type_id' not in json_text                                               # No type IDs
        assert 'predicate_id' not in json_text
        assert 'ontology_id'  not in json_text
        assert 'graph_id'     not in json_text

    def test__project__nodes_have_ref_and_name(self):                                        # Node structure
        projected = self.projector.project(self.graph)

        for node in projected.projection.nodes:
            assert type(node)      is Schema__Projected__Node
            assert type(node.ref)  is Node_Type_Ref
            assert type(node.name) is Safe_Str__Id

    def test__project__edges_have_from_to_ref(self):                                         # Edge structure
        projected = self.projector.project(self.graph)

        for edge in projected.projection.edges:
            assert type(edge)           is Schema__Projected__Edge
            assert type(edge.from_name) is Safe_Str__Id
            assert type(edge.to_name)   is Safe_Str__Id
            assert type(edge.ref)       is Predicate_Ref

    # ═══════════════════════════════════════════════════════════════════════════
    # Reverse Lookup Builder Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__build_node_type_id_to_ref(self):                                               # Test ID → Ref mapping for node types
        id_to_ref = self.projector.build_node_type_id_to_ref(self.ontology)

        assert type(id_to_ref) is dict
        assert len(id_to_ref)  == len(self.ontology.node_types)

        for node_type_id, node_type_ref in id_to_ref.items():                                # Check types
            assert type(node_type_id)  is Node_Type_Id
            assert type(node_type_ref) is Node_Type_Ref

    def test__build_node_type_id_to_ref__with_none_ontology(self):                           # Handles missing ontology
        id_to_ref = self.projector.build_node_type_id_to_ref(None)

        assert id_to_ref == {}

    def test__build_predicate_id_to_ref(self):                                               # Test ID → Ref mapping for predicates
        id_to_ref = self.projector.build_predicate_id_to_ref(self.ontology)

        assert type(id_to_ref) is dict
        assert len(id_to_ref)  == len(self.ontology.predicates)

        for predicate_id, predicate_ref in id_to_ref.items():                                # Check types
            assert type(predicate_id)  is Predicate_Id
            assert type(predicate_ref) is Predicate_Ref

    def test__build_predicate_id_to_ref__with_none_ontology(self):                           # Handles missing ontology
        id_to_ref = self.projector.build_predicate_id_to_ref(None)

        assert id_to_ref == {}

    def test__build_node_id_to_name(self):                                                   # Test Node_Id → name mapping
        id_to_name = self.projector.build_node_id_to_name(self.graph)

        assert type(id_to_name) is dict
        assert len(id_to_name)  == len(self.graph.nodes)

    # ═══════════════════════════════════════════════════════════════════════════
    # Projection Method Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__project_nodes(self):                                                           # Test node projection
        id_to_ref = self.projector.build_node_type_id_to_ref(self.ontology)
        nodes     = self.projector.project_nodes(self.graph, id_to_ref, {})

        assert type(nodes) is List__Projected__Nodes
        assert len(nodes)  == 4                                                              # 4 nodes in test graph

    def test__project_nodes__unknown_type_uses_empty_ref(self):                              # Handles unknown node types
        id_to_ref = {}                                                                       # Empty mapping
        nodes     = self.projector.project_nodes(self.graph, id_to_ref, {})

        for node in nodes:
            assert str(node.ref) == ''                                                       # Falls back to empty ref

    def test__project_edges(self):                                                           # Test edge projection
        id_to_name              = self.projector.build_node_id_to_name    (self.graph)
        id_to_ref               = self.projector.build_predicate_id_to_ref(self.ontology)
        property_name_id_to_ref = self.projector.build_node_type_id_to_ref(self.ontology)
        edges                   = self.projector.project_edges(self.graph, id_to_name, id_to_ref, property_name_id_to_ref)

        assert type(edges) is List__Projected__Edges
        assert len(edges)  == 4                                                              # 4 edges in test graph

    def test__project_edges__unknown_node_uses_empty_name(self):                             # Handles unknown node IDs
        id_to_name              = {}                                                                     # Empty mapping
        id_to_ref               = self.projector.build_predicate_id_to_ref(self.ontology)
        property_name_id_to_ref = self.projector.build_node_type_id_to_ref(self.ontology)
        edges                   = self.projector.project_edges(self.graph, id_to_name, id_to_ref, property_name_id_to_ref)

        for edge in edges:
            assert str(edge.from_name) == ''                                                 # Falls back to empty name
            assert str(edge.to_name)   == ''

    def test__project_edges__unknown_predicate_uses_empty_ref(self):                         # Handles unknown predicates
        id_to_name              = self.projector.build_node_id_to_name(self.graph)
        id_to_ref               = {}                                                                      # Empty mapping
        property_name_id_to_ref = self.projector.build_node_type_id_to_ref(self.ontology)
        edges                   = self.projector.project_edges(self.graph, id_to_name, id_to_ref, property_name_id_to_ref)

        for edge in edges:
            assert str(edge.ref) == ''                                                       # Falls back to empty ref

    # ═══════════════════════════════════════════════════════════════════════════
    # References Builder Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__build_references__enables_correlation(self):                                   # References for tooling
        projected = self.projector.project(self.graph)

        # Can look up node type ID by ref
        for node_type_ref in projected.references.node_types.keys():
            node_type_id = projected.references.node_types.get(node_type_ref)
            assert node_type_id is not None
            assert type(node_type_id) is Node_Type_Id

        # Can look up predicate ID by ref
        for predicate_ref in projected.references.predicates.keys():
            predicate_id = projected.references.predicates.get(predicate_ref)
            assert predicate_id is not None
            assert type(predicate_id) is Predicate_Id

    # ═══════════════════════════════════════════════════════════════════════════
    # Sources Builder Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__build_sources(self):                                                           # Test sources section
        sources = self.projector.build_sources(self.graph, self.ontology)

        assert type(sources)                is Schema__Projected__Sources
        assert type(sources.source_graph_id) is Graph_Id
        assert type(sources.generated_at)    is Timestamp_Now

    def test__build_sources__captures_graph_id(self):                                        # Sources tracks source graph
        sources = self.projector.build_sources(self.graph, self.ontology)

        assert sources.source_graph_id == self.graph.graph_id

    def test__build_sources__with_none_ontology(self):                                       # Handles missing ontology
        sources = self.projector.build_sources(self.graph, None)

        assert sources.source_graph_id == self.graph.graph_id
        assert sources.ontology_seed   is None

    def test__build_sources__enables_tracing(self):                                          # Provenance for debugging
        projected = self.projector.project(self.graph)

        assert projected.sources.source_graph_id == self.graph.graph_id                      # Can trace to source
        assert projected.sources.generated_at    is not None                                 # Has timestamp

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════

    def test__project__empty_graph(self):                                                    # Handles empty graph
        empty_graph = self.test_data.create_graph__empty()
        empty_ont_registry = Ontology__Registry()
        empty_tax_registry = Taxonomy__Registry()
        projector = Semantic_Graph__Projector(ontology_registry = empty_ont_registry,
                                              taxonomy_registry = empty_tax_registry)

        projected = projector.project(empty_graph)

        assert type(projected)                 is Schema__Projected__Semantic_Graph
        assert len(projected.projection.nodes) == 0
        assert len(projected.projection.edges) == 0

    def test__project__graph_without_registered_ontology(self):                              # Graph refs unregistered ontology
        unregistered_graph = Schema__Semantic_Graph(graph_id    = Graph_Id(Obj_Id())              ,
                                                    ontology_id = Ontology_Id(Obj_Id())           ,
                                                    nodes       = Dict__Nodes__By_Id()            ,
                                                    edges       = List__Semantic_Graph__Edges()   )
        projector = Semantic_Graph__Projector(ontology_registry = Ontology__Registry(),
                                              taxonomy_registry = Taxonomy__Registry())

        projected = projector.project(unregistered_graph)                                    # Should not raise

        assert type(projected) is Schema__Projected__Semantic_Graph
        assert len(projected.references.node_types) == 0                                     # Empty references (no ontology)
        assert len(projected.references.predicates) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Determinism Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__project__is_deterministic_for_projection(self):                                # Same input → same projection
        projected_1 = self.projector.project(self.graph)
        projected_2 = self.projector.project(self.graph)

        assert projected_1.projection.json() == projected_2.projection.json()                # Projection is stable

    def test__project__is_deterministic_for_references(self):                                # Same input → same references
        projected_1 = self.projector.project(self.graph)
        projected_2 = self.projector.project(self.graph)

        assert projected_1.references.json() == projected_2.references.json()                # References are stable

    def test__project__sources_graph_id_is_stable(self):                                     # Source graph ID is consistent
        projected_1 = self.projector.project(self.graph)
        projected_2 = self.projector.project(self.graph)

        assert projected_1.sources.source_graph_id == projected_2.sources.source_graph_id

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with Complete Fixture
    # ═══════════════════════════════════════════════════════════════════════════

    def test__fixture_projection_matches(self):                                              # Fixture provides consistent projection
        fixture_projection = self.fixture['projection']
        computed_projection = self.projector.project(self.graph)

        assert len(fixture_projection.projection.nodes) == len(computed_projection.projection.nodes)
        assert len(fixture_projection.projection.edges) == len(computed_projection.projection.edges)