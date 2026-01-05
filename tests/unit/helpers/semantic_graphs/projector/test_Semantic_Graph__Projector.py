# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic_Graph__Projector - Tests for Schema__ to Projected__ transformation
#
# Brief 3.7 Compliance:
#   - Projection contains NO IDs (only refs and names)
#   - Three sections: projection, references, sources
#   - One-way transformation (generated, not edited)
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                                 import TestCase
from osbot_utils.helpers.semantic_graphs.ontology.Ontology__Registry                          import Ontology__Registry
from osbot_utils.helpers.semantic_graphs.projector.Semantic_Graph__Projector                  import Semantic_Graph__Projector
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Type_Ids__By_Ref       import Dict__Node_Type_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id                import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Predicate_Ids__By_Ref       import Dict__Predicate_Ids__By_Ref
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Projected__Edges            import List__Projected__Edges
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Projected__Nodes            import List__Projected__Nodes
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges       import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph                 import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                      import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref                     import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id                       import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                      import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Ref                     import Predicate_Ref
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Data            import Schema__Projected__Data
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Edge            import Schema__Projected__Edge
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Node            import Schema__Projected__Node
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__References      import Schema__Projected__References
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Semantic_Graph  import Schema__Projected__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.projected.Schema__Projected__Sources         import Schema__Projected__Sources
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data               import QA__Semantic_Graphs__Test_Data
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data               import EXPECTED__PROJECTED__SIMPLE_CLASS__NODES
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data               import EXPECTED__PROJECTED__SIMPLE_CLASS__EDGES
from osbot_utils.testing.__ import __, __SKIP__
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                            import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_int.Timestamp_Now              import Timestamp_Now
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id               import Safe_Str__Id


class test_Semantic_Graph__Projector(TestCase):                                              # Test projector transformation

    @classmethod
    def setUpClass(cls):                                                                     # Shared setup
        cls.test_data = QA__Semantic_Graphs__Test_Data()
        cls.registry, cls.graph = cls.test_data.create_projection_test_setup()
        cls.ontology  = cls.registry.get_by_id(cls.graph.ontology_id)
        cls.projector = Semantic_Graph__Projector(ontology_registry = cls.registry)

    def test__init__(self):                                                                  # Test basic initialization
        with Semantic_Graph__Projector() as _:
            assert type(_)                   is Semantic_Graph__Projector
            assert type(_.ontology_registry) is Ontology__Registry

    def test__init__with_registry(self):                                                     # Test initialization with registry
        registry  = Ontology__Registry()
        projector = Semantic_Graph__Projector(ontology_registry = registry)

        assert projector.ontology_registry is registry

    # ═══════════════════════════════════════════════════════════════════════════
    # Main Project Method Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__project(self):                                                                 # Test main projection method
        projected = self.projector.project(self.graph)

        assert type(projected)            is Schema__Projected__Semantic_Graph
        assert type(projected.projection) is Schema__Projected__Data
        assert type(projected.references) is Schema__Projected__References
        assert type(projected.sources)    is Schema__Projected__Sources

    def test__project__returns_three_sections(self):                                         # Brief 3.7: exactly three sections
        projected = self.projector.project(self.graph)

        assert projected.obj() == __(  projection=__(nodes=[__(ref='module', name='my_module'),
                                                            __(ref='class', name='MyClass'),
                                                            __(ref='method', name='my_method')],
                                                     edges=[__(from_name='my_module',
                                                               to_name='MyClass',
                                                               ref='contains'),
                                                            __(from_name='MyClass',
                                                               to_name='my_method',
                                                               ref='contains')]),
                                       references=__(nodes=__(module='d84ade10',
                                                              _class='2a530b24',
                                                              method='99a23b6f',
                                                              function='45305464'),
                                                     edges=__(contains='b8dbb70e',
                                                              _in='c35666f3',
                                                              calls='f9520a72',
                                                              called_by='a4232771')),
                                       sources=__(ontology_seed=None,
                                                  source_graph_id='c13f47de',
                                                  generated_at=__SKIP__))

        assert self.graph.obj() == __( graph_id_source=None,
                                       rule_set_id='d01d41cc',
                                       graph_id='c13f47de',
                                       ontology_id='c6c846c6',
                                       nodes=__(ff5bcf64=__(node_id_source=__(source_type='deterministic',
                                                                              seed='test:node:my_module'),
                                                            node_id='ff5bcf64',
                                                            node_type_id='d84ade10',
                                                            name='my_module'),
                                                _02a4d1fa=__(node_id_source=__(source_type='deterministic',
                                                                               seed='test:node:MyClass'),
                                                             node_id='02a4d1fa',
                                                             node_type_id='2a530b24',
                                                             name='MyClass'),
                                                _53b63bbe=__(node_id_source=__(source_type='deterministic',
                                                                               seed='test:node:my_method'),
                                                             node_id='53b63bbe',
                                                             node_type_id='99a23b6f',
                                                             name='my_method')),
                                       edges=[__(edge_id_source=__(source_type='deterministic',
                                                                   seed='test:edge:module_contains_class'),
                                                 edge_id='fa07486e',
                                                 from_node_id='ff5bcf64',
                                                 to_node_id='02a4d1fa',
                                                 predicate_id='b8dbb70e'),
                                              __(edge_id_source=__(source_type='deterministic',
                                                                   seed='test:edge:class_contains_method'),
                                                 edge_id='95e10d20',
                                                 from_node_id='02a4d1fa',
                                                 to_node_id='53b63bbe',
                                                 predicate_id='b8dbb70e')])

        assert self.ontology.obj()   == __(ontology_id_source=None,
                                           description='Python code structure ontology',
                                           taxonomy_id='5fb24b5a',
                                           ontology_id='c6c846c6',
                                           ontology_ref='code_structure',
                                           node_types=__(d84ade10=__(node_type_id_source=__(source_type='deterministic',
                                                                                            seed='test:node_type:module'),
                                                                     description='Python module',
                                                                     node_type_id='d84ade10',
                                                                     node_type_ref='module'),
                                                         _2a530b24=__(node_type_id_source=__(source_type='deterministic',
                                                                                             seed='test:node_type:class'),
                                                                      description='Python class',
                                                                      node_type_id='2a530b24',
                                                                      node_type_ref='class'),
                                                         _99a23b6f=__(node_type_id_source=__(source_type='deterministic',
                                                                                             seed='test:node_type:method'),
                                                                      description='Class method',
                                                                      node_type_id='99a23b6f',
                                                                      node_type_ref='method'),
                                                         _45305464=__(node_type_id_source=__(source_type='deterministic',
                                                                                             seed='test:node_type:function'),
                                                                      description='Standalone function',
                                                                      node_type_id='45305464',
                                                                      node_type_ref='function')),
                                           predicates=__(b8dbb70e=__(predicate_id_source=__(source_type='deterministic',
                                                                                            seed='test:predicate:contains'),
                                                                     inverse_id='c35666f3',
                                                                     description='Contains child',
                                                                     predicate_id='b8dbb70e',
                                                                     predicate_ref='contains'),
                                                         c35666f3=__(predicate_id_source=__(source_type='deterministic',
                                                                                            seed='test:predicate:in'),
                                                                     inverse_id='b8dbb70e',
                                                                     description='Is contained in',
                                                                     predicate_id='c35666f3',
                                                                     predicate_ref='in'),
                                                         f9520a72=__(predicate_id_source=__(source_type='deterministic',
                                                                                            seed='test:predicate:calls'),
                                                                     inverse_id='a4232771',
                                                                     description='Calls',
                                                                     predicate_id='f9520a72',
                                                                     predicate_ref='calls'),
                                                         a4232771=__(predicate_id_source=__(source_type='deterministic',
                                                                                            seed='test:predicate:called_by'),
                                                                     inverse_id='f9520a72',
                                                                     description='Called by',
                                                                     predicate_id='a4232771',
                                                                     predicate_ref='called_by')),
                                           edge_rules=[__(source_type_id='d84ade10',
                                                          predicate_id='b8dbb70e',
                                                          target_type_id='2a530b24'),
                                                       __(source_type_id='d84ade10',
                                                          predicate_id='b8dbb70e',
                                                          target_type_id='99a23b6f'),
                                                       __(source_type_id='d84ade10',
                                                          predicate_id='b8dbb70e',
                                                          target_type_id='45305464'),
                                                       __(source_type_id='2a530b24',
                                                          predicate_id='b8dbb70e',
                                                          target_type_id='99a23b6f'),
                                                       __(source_type_id='2a530b24',
                                                          predicate_id='c35666f3',
                                                          target_type_id='d84ade10'),
                                                       __(source_type_id='99a23b6f',
                                                          predicate_id='c35666f3',
                                                          target_type_id='d84ade10'),
                                                       __(source_type_id='99a23b6f',
                                                          predicate_id='c35666f3',
                                                          target_type_id='2a530b24'),
                                                       __(source_type_id='45305464',
                                                          predicate_id='c35666f3',
                                                          target_type_id='d84ade10'),
                                                       __(source_type_id='99a23b6f',
                                                          predicate_id='f9520a72',
                                                          target_type_id='99a23b6f'),
                                                       __(source_type_id='99a23b6f',
                                                          predicate_id='f9520a72',
                                                          target_type_id='45305464'),
                                                       __(source_type_id='45305464',
                                                          predicate_id='f9520a72',
                                                          target_type_id='99a23b6f'),
                                                       __(source_type_id='45305464',
                                                          predicate_id='f9520a72',
                                                          target_type_id='45305464')])


    def test__project__projection_has_nodes_and_edges(self):                                 # Projection section structure
        projected = self.projector.project(self.graph)

        assert type(projected.projection.nodes) is List__Projected__Nodes
        assert type(projected.projection.edges) is List__Projected__Edges
        assert len(projected.projection.nodes)  == 3                                         # module, class, method
        assert len(projected.projection.edges)  == 2                                         # two contains edges

    def test__project__node_count_matches_graph(self):                                       # Projected nodes match source
        projected = self.projector.project(self.graph)

        assert len(projected.projection.nodes) == len(self.graph.nodes)

    def test__project__edge_count_matches_graph(self):                                       # Projected edges match source
        projected = self.projector.project(self.graph)

        assert len(projected.projection.edges) == len(self.graph.edges)

    # ═══════════════════════════════════════════════════════════════════════════
    # Brief 3.7 Compliance: No IDs in Projection
    # ═══════════════════════════════════════════════════════════════════════════

    def test__project__projection_contains_no_ids(self):                                     # Key Brief 3.7 requirement
        projected = self.projector.project(self.graph)

        json_str = projected.projection.json()

        assert 'node_id'      not in json_str                                                # No instance IDs
        assert 'edge_id'      not in json_str
        assert 'node_type_id' not in json_str                                                # No type IDs
        assert 'predicate_id' not in json_str
        assert 'ontology_id'  not in json_str
        assert 'graph_id'     not in json_str

    def test__project__projection_has_refs_and_names(self):                                  # Human-readable fields present
        projected = self.projector.project(self.graph)

        json_str = projected.projection.json()

        assert json_str == { 'edges': [{'from_name': 'my_module', 'ref': 'contains', 'to_name': 'MyClass'},
                                       {'from_name': 'MyClass', 'ref': 'contains', 'to_name': 'my_method'}],
                             'nodes': [{'name': 'my_module', 'ref': 'module'},
                                       {'name': 'MyClass', 'ref': 'class'},
                                       {'name': 'my_method', 'ref': 'method'}]}

    def test__project__nodes_have_ref_and_name_only(self):                                   # Node structure per Brief 3.7
        projected = self.projector.project(self.graph)

        for node in projected.projection.nodes:
            assert type(node)      is Schema__Projected__Node
            assert type(node.ref)  is Node_Type_Ref
            assert type(node.name) is Safe_Str__Id
            assert node.obj()      == __(ref=__SKIP__,
                                         name=__SKIP__)                     # Exactly two fields

    def test__project__edges_have_from_to_ref_only(self):                                    # Edge structure per Brief 3.7
        projected = self.projector.project(self.graph)

        for edge in projected.projection.edges:
            assert type(edge)           is Schema__Projected__Edge
            assert type(edge.from_name) is Safe_Str__Id
            assert type(edge.to_name)   is Safe_Str__Id
            assert type(edge.ref)       is Predicate_Ref
            assert edge.obj()           == __(from_name = __SKIP__,
                                              to_name   = __SKIP__,
                                              ref       = __SKIP__)     # Exactly three fields

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

        names = list(id_to_name.values())
        assert Safe_Str__Id('my_module') in names
        assert Safe_Str__Id('MyClass')   in names
        assert Safe_Str__Id('my_method') in names

    # ═══════════════════════════════════════════════════════════════════════════
    # Projection Method Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__project_nodes(self):                                                           # Test node projection
        id_to_ref = self.projector.build_node_type_id_to_ref(self.ontology)
        nodes     = self.projector.project_nodes(self.graph, id_to_ref)

        assert type(nodes) is List__Projected__Nodes
        assert len(nodes)  == 3

        node_data = [(str(n.ref), str(n.name)) for n in nodes]
        assert ('module', 'my_module') in node_data
        assert ('class',  'MyClass')   in node_data
        assert ('method', 'my_method') in node_data

    def test__project_nodes__unknown_type_uses_empty_ref(self):                              # Handles unknown node types
        id_to_ref = {}                                                                       # Empty mapping
        nodes     = self.projector.project_nodes(self.graph, id_to_ref)

        for node in nodes:
            assert str(node.ref) == ''                                                       # Falls back to empty ref

    def test__project_edges(self):                                                           # Test edge projection
        id_to_name  = self.projector.build_node_id_to_name(self.graph)
        id_to_ref   = self.projector.build_predicate_id_to_ref(self.ontology)
        edges       = self.projector.project_edges(self.graph, id_to_name, id_to_ref)

        assert type(edges) is List__Projected__Edges
        assert len(edges)  == 2

        edge_data = [(str(e.from_name), str(e.to_name), str(e.ref)) for e in edges]
        assert ('my_module', 'MyClass',   'contains') in edge_data
        assert ('MyClass',   'my_method', 'contains') in edge_data

    def test__project_edges__unknown_node_uses_empty_name(self):                             # Handles unknown node IDs
        id_to_name  = {}                                                                     # Empty mapping
        id_to_ref   = self.projector.build_predicate_id_to_ref(self.ontology)
        edges       = self.projector.project_edges(self.graph, id_to_name, id_to_ref)

        for edge in edges:
            assert str(edge.from_name) == ''                                                 # Falls back to empty name
            assert str(edge.to_name)   == ''

    def test__project_edges__unknown_predicate_uses_empty_ref(self):                         # Handles unknown predicates
        id_to_name = self.projector.build_node_id_to_name(self.graph)
        id_to_ref  = {}                                                                      # Empty mapping
        edges      = self.projector.project_edges(self.graph, id_to_name, id_to_ref)

        for edge in edges:
            assert str(edge.ref) == ''                                                       # Falls back to empty ref

    # ═══════════════════════════════════════════════════════════════════════════
    # References Builder Tests
    # ═══════════════════════════════════════════════════════════════════════════

    def test__build_references(self):                                                        # Test references section
        node_type_id_to_ref = self.projector.build_node_type_id_to_ref(self.ontology)
        predicate_id_to_ref = self.projector.build_predicate_id_to_ref(self.ontology)
        references          = self.projector.build_references(node_type_id_to_ref, predicate_id_to_ref)

        assert type(references)       is Schema__Projected__References
        assert type(references.nodes) is Dict__Node_Type_Ids__By_Ref
        assert type(references.edges) is Dict__Predicate_Ids__By_Ref

    def test__build_references__inverts_mapping(self):                                       # References invert ID→Ref to Ref→ID
        node_type_id_to_ref = self.projector.build_node_type_id_to_ref(self.ontology)
        predicate_id_to_ref = self.projector.build_predicate_id_to_ref(self.ontology)
        references          = self.projector.build_references(node_type_id_to_ref, predicate_id_to_ref)

        for node_type_id, node_type_ref in node_type_id_to_ref.items():                      # Can look up ID by ref
            assert references.nodes.get(node_type_ref) == node_type_id

        for predicate_id, predicate_ref in predicate_id_to_ref.items():                      # Can look up ID by ref
            assert references.edges.get(predicate_ref) == predicate_id

    def test__build_references__enables_correlation(self):                                   # Brief 3.7: references for tooling
        projected = self.projector.project(self.graph)

        class_id = projected.references.nodes.get(Node_Type_Ref('class'))                    # Look up node type ID
        assert class_id is not None
        assert type(class_id) is Node_Type_Id

        contains_id = projected.references.edges.get(Predicate_Ref('contains'))              # Look up predicate ID
        assert contains_id is not None
        assert type(contains_id) is Predicate_Id

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

    def test__build_sources__captures_ontology_seed(self):                                   # Sources tracks ontology seed
        sources = self.projector.build_sources(self.graph, self.ontology)

        if self.ontology.ontology_id_source:
            assert sources.ontology_seed == self.ontology.ontology_id_source.seed
        else:
            assert sources.ontology_seed is None

    def test__build_sources__with_none_ontology(self):                                       # Handles missing ontology
        sources = self.projector.build_sources(self.graph, None)

        assert sources.source_graph_id == self.graph.graph_id
        assert sources.ontology_seed   is None

    def test__build_sources__enables_tracing(self):                                          # Brief 3.7: provenance for debugging
        projected = self.projector.project(self.graph)

        assert projected.sources.source_graph_id == self.graph.graph_id                      # Can trace to source
        assert projected.sources.generated_at    is not None                                 # Has timestamp

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Cases
    # ═══════════════════════════════════════════════════════════════════════════

    def test__project__empty_graph(self):                                                    # Handles empty graph
        empty_graph = self.test_data.create_graph__empty()
        empty_registry = Ontology__Registry()
        projector = Semantic_Graph__Projector(ontology_registry = empty_registry)

        projected = projector.project(empty_graph)

        assert type(projected)                 is Schema__Projected__Semantic_Graph
        assert len(projected.projection.nodes) == 0
        assert len(projected.projection.edges) == 0

    def test__project__graph_without_registered_ontology(self):                              # Graph refs unregistered ontology
        unregistered_graph = Schema__Semantic_Graph(graph_id    = Graph_Id(Obj_Id())              ,
                                                    ontology_id = Ontology_Id(Obj_Id())           ,
                                                    nodes       = Dict__Nodes__By_Id()            ,
                                                    edges       = List__Semantic_Graph__Edges()   )
        projector = Semantic_Graph__Projector(ontology_registry = Ontology__Registry())

        projected = projector.project(unregistered_graph)                                    # Should not raise

        assert type(projected) is Schema__Projected__Semantic_Graph
        assert len(projected.references.nodes) == 0                                          # Empty references (no ontology)
        assert len(projected.references.edges) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with Expected Output
    # ═══════════════════════════════════════════════════════════════════════════

    def test__project__matches_expected_nodes(self):                                         # Output matches expected constants
        projected = self.projector.project(self.graph)

        projected_nodes = [n.obj() for n in projected.projection.nodes]

        for expected in EXPECTED__PROJECTED__SIMPLE_CLASS__NODES:
            assert __(ref = expected['ref'], name = expected['name']) in projected_nodes

    def test__project__matches_expected_edges(self):                                         # Output matches expected constants
        projected = self.projector.project(self.graph)

        projected_edges = [e.obj() for e in projected.projection.edges]

        for expected in EXPECTED__PROJECTED__SIMPLE_CLASS__EDGES:
            assert __(from_name = expected['from_name'],
                      to_name   = expected['to_name'  ],
                      ref       = expected['ref'      ]) in projected_edges

    def test__project__matches_expected_factory(self):                                       # Matches QA factory output
        projected     = self.projector.project(self.graph)
        expected_data = self.test_data.create_projected__simple_class__expected()

        projected_nodes = set((str(n.ref), str(n.name)) for n in projected.projection.nodes)
        expected_nodes  = set((str(n.ref), str(n.name)) for n in expected_data.nodes)
        assert projected_nodes == expected_nodes

        projected_edges = set((str(e.from_name), str(e.to_name), str(e.ref)) for e in projected.projection.edges)
        expected_edges  = set((str(e.from_name), str(e.to_name), str(e.ref)) for e in expected_data.edges)
        assert projected_edges == expected_edges

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