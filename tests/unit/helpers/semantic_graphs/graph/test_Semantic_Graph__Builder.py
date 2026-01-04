# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic_Graph__Builder - Tests for graph builder fluent API
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Builder                  import Semantic_Graph__Builder
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Utils                    import Semantic_Graph__Utils
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Nodes__By_Id          import Dict__Nodes__By_Id
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Semantic_Graph__Edges import List__Semantic_Graph__Edges
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph           import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref               import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Ref                import Ontology_Ref
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Rule_Set_Ref                import Rule_Set_Ref
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb      import Safe_Str__Ontology__Verb
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data         import QA__Semantic_Graphs__Test_Data
from osbot_utils.type_safe.primitives.core.Safe_UInt                                    import Safe_UInt
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Version         import Safe_Str__Version
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                      import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                       import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id         import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id__Seed   import Safe_Str__Id__Seed


class test_Semantic_Graph__Builder(TestCase):                                           # Test graph builder

    @classmethod
    def setUpClass(cls):                                                                # Shared test objects (performance)
        cls.qa          = QA__Semantic_Graphs__Test_Data()
        cls.graph_utils = Semantic_Graph__Utils()
        cls.ontology    = cls.qa.create_ontology__code_structure()                      # Reuse across tests
        cls.rule_set    = cls.qa.create_rule_set__code_structure()

    def test__init__(self):                                                             # Test initialization
        with Semantic_Graph__Builder() as _:
            assert type(_.graph)       is Schema__Semantic_Graph
            assert type(_.graph.nodes) is Dict__Nodes__By_Id
            assert type(_.graph.edges) is List__Semantic_Graph__Edges
            assert len(_.graph.nodes)  == 0
            assert len(_.graph.edges)  == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Configuration Methods
    # ═══════════════════════════════════════════════════════════════════════════

    def test__with_ontology(self):                                                      # Test setting ontology ref
        with Semantic_Graph__Builder() as _:
            result = _.with_ontology(Ontology_Ref('test_ontology'))

            assert result is _                                                          # Returns self for chaining
            assert str(_.graph.ontology_ref) == 'test_ontology'

    def test__with_rule_set(self):                                                      # Test setting rule set ref
        with Semantic_Graph__Builder() as _:
            result = _.with_rule_set(Rule_Set_Ref('test_rules'))

            assert result is _                                                          # Returns self for chaining
            assert str(_.graph.rule_set_ref) == 'test_rules'

    def test__with_version(self):                                                       # Test setting version
        with Semantic_Graph__Builder() as _:
            result = _.with_version(Safe_Str__Version('2.0.0'))

            assert result is _
            assert str(_.graph.version) == '2.0.0'

    def test__with_graph_id(self):                                                      # Test setting explicit graph ID
        with Semantic_Graph__Builder() as _:
            explicit_id = Graph_Id(Obj_Id())
            result      = _.with_graph_id(explicit_id)

            assert result is _
            assert _.graph.graph_id == explicit_id

    def test__with_deterministic_graph_id(self):                                        # Test deterministic graph ID
        seed = Safe_Str__Id__Seed('test:builder:graph')

        with Semantic_Graph__Builder() as builder_1:
            builder_1.with_deterministic_graph_id(seed)
            graph_id_1 = builder_1.graph.graph_id

        with Semantic_Graph__Builder() as builder_2:
            builder_2.with_deterministic_graph_id(seed)
            graph_id_2 = builder_2.graph.graph_id

        assert graph_id_1 == graph_id_2                                                 # Same seed → same ID
        assert builder_1.graph.graph_id_source is not None
        assert str(builder_1.graph.graph_id_source.seed) == 'test:builder:graph'

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__add_node(self):                                                           # Test adding nodes
        with Semantic_Graph__Builder() as _:
            result = _.add_node(node_type   = Node_Type_Ref('class')  ,
                                name        = Safe_Str__Id('MyClass') ,
                                line_number = Safe_UInt(10)           )

            assert result is _                                                          # Returns self for chaining
            assert len(_.graph.nodes) == 1

            node = list(_.graph.nodes.values())[0]
            assert str(node.node_type)   == 'class'
            assert str(node.name)        == 'MyClass'
            assert int(node.line_number) == 10

    def test__add_node__with_explicit_id(self):                                         # Test adding node with explicit ID
        with Semantic_Graph__Builder() as _:
            explicit_id = Node_Id(Obj_Id())
            _.add_node(node_type = Node_Type_Ref('method')   ,
                       name      = Safe_Str__Id('my_method') ,
                       node_id   = explicit_id               )

            assert explicit_id in _.graph.nodes
            assert str(_.graph.nodes[explicit_id].name) == 'my_method'

    def test__add_node_with_seed(self):                                                 # Test adding node with deterministic ID
        seed = Safe_Str__Id__Seed('test:node:class')

        with Semantic_Graph__Builder() as builder_1:
            builder_1.add_node_with_seed(node_type = Node_Type_Ref('class')             ,
                                         name      = Safe_Str__Id('DeterministicClass') ,
                                         seed      = seed                               )
            node_1 = list(builder_1.graph.nodes.values())[0]

        with Semantic_Graph__Builder() as builder_2:
            builder_2.add_node_with_seed(node_type = Node_Type_Ref('class')             ,
                                         name      = Safe_Str__Id('DeterministicClass') ,
                                         seed      = seed                               )
            node_2 = list(builder_2.graph.nodes.values())[0]

        assert node_1.node_id == node_2.node_id                                         # Same seed → same ID
        assert node_1.node_id_source is not None
        assert str(node_1.node_id_source.seed) == 'test:node:class'

    def test__add_multiple_nodes(self):                                                 # Test adding multiple nodes
        with Semantic_Graph__Builder() as _:
            _.add_node(Node_Type_Ref('module')  , Safe_Str__Id('my_module'))
            _.add_node(Node_Type_Ref('class')   , Safe_Str__Id('MyClass'))
            _.add_node(Node_Type_Ref('method')  , Safe_Str__Id('my_method'))

            assert len(_.graph.nodes) == 3

            node_types = [str(n.node_type) for n in _.graph.nodes.values()]
            assert 'module' in node_types
            assert 'class'  in node_types
            assert 'method' in node_types

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__add_edge(self):                                                           # Test adding edges
        with Semantic_Graph__Builder() as _:
            _.add_node_with_seed(Node_Type_Ref('class') , Safe_Str__Id('A')  , Safe_Str__Id__Seed('test:a'))
            _.add_node_with_seed(Node_Type_Ref('method'), Safe_Str__Id('foo'), Safe_Str__Id__Seed('test:foo'))

            node_ids = list(_.graph.nodes.keys())
            node_a   = node_ids[0]
            node_foo = node_ids[1]

            result = _.add_edge(from_node = node_a                               ,
                                verb      = Safe_Str__Ontology__Verb('contains') ,
                                to_node   = node_foo                             )

            assert result is _                                                          # Returns self for chaining
            assert len(_.graph.edges) == 1

            edge = _.graph.edges[0]
            assert edge.from_node    == node_a
            assert str(edge.verb)    == 'contains'
            assert edge.to_node      == node_foo

    def test__add_edge_with_seed(self):                                                 # Test adding edge with deterministic ID
        with Semantic_Graph__Builder() as _:
            _.add_node_with_seed(Node_Type_Ref('class') , Safe_Str__Id('A')  , Safe_Str__Id__Seed('test:a'))
            _.add_node_with_seed(Node_Type_Ref('method'), Safe_Str__Id('foo'), Safe_Str__Id__Seed('test:foo'))

            node_ids = list(_.graph.nodes.keys())
            node_a   = node_ids[0]
            node_foo = node_ids[1]

            _.add_edge_with_seed(from_node = node_a                               ,
                                 verb      = Safe_Str__Ontology__Verb('contains') ,
                                 to_node   = node_foo                             ,
                                 seed      = Safe_Str__Id__Seed('test:edge:a_contains_foo'))

            edge = _.graph.edges[0]
            assert edge.edge_id_source is not None
            assert str(edge.edge_id_source.seed) == 'test:edge:a_contains_foo'

    def test__add_edge_with_line_number(self):                                          # Test edge with source location
        with Semantic_Graph__Builder() as _:
            _.add_node_with_seed(Node_Type_Ref('method'), Safe_Str__Id('caller'), Safe_Str__Id__Seed('test:caller'))
            _.add_node_with_seed(Node_Type_Ref('method'), Safe_Str__Id('callee'), Safe_Str__Id__Seed('test:callee'))

            node_ids = list(_.graph.nodes.keys())
            caller = node_ids[0]
            callee = node_ids[1]

            _.add_edge(from_node   = caller                          ,
                       verb        = Safe_Str__Ontology__Verb('calls'),
                       to_node     = callee                          ,
                       line_number = Safe_UInt(42)                   )

            edge = _.graph.edges[0]
            assert int(edge.line_number) == 42

    # ═══════════════════════════════════════════════════════════════════════════
    # Build Operation
    # ═══════════════════════════════════════════════════════════════════════════

    def test__build(self):                                                              # Test building final graph
        with Semantic_Graph__Builder() as _:
            _.with_ontology(Ontology_Ref('code_structure'))
            _.with_rule_set(Rule_Set_Ref('code_rules'))
            _.add_node(Node_Type_Ref('class'), Safe_Str__Id('A'))
            _.add_node(Node_Type_Ref('class'), Safe_Str__Id('B'))

            graph = _.build()

            assert type(graph)              is Schema__Semantic_Graph
            assert str(graph.ontology_ref)  == 'code_structure'
            assert str(graph.rule_set_ref)  == 'code_rules'
            assert self.graph_utils.node_count(graph) == 2

    def test__build__returns_same_graph(self):                                          # Test build returns internal graph
        with Semantic_Graph__Builder() as _:
            _.add_node(Node_Type_Ref('class'), Safe_Str__Id('Test'))

            graph = _.build()

            assert graph is _.graph                                                     # Same object, not copy

    # ═══════════════════════════════════════════════════════════════════════════
    # Fluent API Chaining
    # ═══════════════════════════════════════════════════════════════════════════

    def test__fluent_api_chaining(self):                                                # Test full fluent API
        with Semantic_Graph__Builder() as _:
            graph = (_.with_ontology(Ontology_Ref('code_structure'))
                      .with_rule_set(Rule_Set_Ref('code_rules'))
                      .with_version(Safe_Str__Version('1.0.0'))
                      .add_node(Node_Type_Ref('module'), Safe_Str__Id('my_module'))
                      .add_node(Node_Type_Ref('class') , Safe_Str__Id('MyClass'))
                      .build())

            assert str(graph.ontology_ref) == 'code_structure'
            assert str(graph.rule_set_ref) == 'code_rules'
            assert str(graph.version)      == '1.0.0'
            assert len(graph.nodes)        == 2

    def test__fluent_api_with_edges(self):                                              # Test chaining with edges
        with Semantic_Graph__Builder() as _:
            _.with_ontology(Ontology_Ref('code_structure'))

            _.add_node_with_seed(Node_Type_Ref('class') , Safe_Str__Id('A')  , Safe_Str__Id__Seed('a'))
            _.add_node_with_seed(Node_Type_Ref('method'), Safe_Str__Id('foo'), Safe_Str__Id__Seed('foo'))

            node_ids  = list(_.graph.nodes.keys())
            class_id  = node_ids[0]
            method_id = node_ids[1]

            _.add_edge(class_id, Safe_Str__Ontology__Verb('contains'), method_id)

            graph = _.build()

            assert self.graph_utils.node_count(graph) == 2
            assert self.graph_utils.edge_count(graph) == 1

    # ═══════════════════════════════════════════════════════════════════════════
    # Integration with QA Test Data
    # ═══════════════════════════════════════════════════════════════════════════

    def test__build_graph_matching_qa_structure(self):                                  # Build same structure as QA graph
        with Semantic_Graph__Builder() as _:
            _.with_ontology(Ontology_Ref('code_structure'))
            _.with_rule_set(Rule_Set_Ref('code_structure_rules'))

            _.add_node_with_seed(Node_Type_Ref('module'), Safe_Str__Id('my_module'), Safe_Str__Id__Seed('test:node:my_module'))
            _.add_node_with_seed(Node_Type_Ref('class') , Safe_Str__Id('MyClass')  , Safe_Str__Id__Seed('test:node:MyClass'))
            _.add_node_with_seed(Node_Type_Ref('method'), Safe_Str__Id('my_method'), Safe_Str__Id__Seed('test:node:my_method'))

            node_ids  = list(_.graph.nodes.keys())
            module_id = node_ids[0]
            class_id  = node_ids[1]
            method_id = node_ids[2]

            _.add_edge(module_id, Safe_Str__Ontology__Verb('contains'), class_id)
            _.add_edge(class_id , Safe_Str__Ontology__Verb('contains'), method_id)

            builder_graph = _.build()

        qa_graph = self.qa.create_graph__simple_class()

        assert len(builder_graph.nodes)  == len(qa_graph.nodes)                         # Same structure
        assert len(builder_graph.edges)  == len(qa_graph.edges)
        assert str(builder_graph.ontology_ref) == str(qa_graph.ontology_ref)

        builder_node_ids = set(str(id) for id in builder_graph.nodes.keys())            # Same deterministic IDs
        qa_node_ids      = set(str(id) for id in qa_graph.nodes.keys())
        assert builder_node_ids == qa_node_ids

    def test__builder_vs_qa__deterministic_nodes(self):                                 # Verify deterministic node IDs match
        with Semantic_Graph__Builder() as _:
            _.add_node_with_seed(Node_Type_Ref('module'), Safe_Str__Id('my_module'), Safe_Str__Id__Seed('test:node:my_module'))
            builder_node_id = list(_.graph.nodes.keys())[0]

        qa_graph   = self.qa.create_graph__simple_class()
        qa_node_id = None
        for node_id, node in qa_graph.nodes.items():
            if str(node.name) == 'my_module':
                qa_node_id = node_id
                break

        assert str(builder_node_id) == str(qa_node_id)                                  # Same seed → same ID