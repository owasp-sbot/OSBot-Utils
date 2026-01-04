# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic_Graph__Utils - Tests for semantic graph utility operations
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Utils                    import Semantic_Graph__Utils
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Node_Ids              import List__Node_Ids
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge     import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node     import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Ref               import Node_Type_Ref
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb      import Safe_Str__Ontology__Verb
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data         import QA__Semantic_Graphs__Test_Data, OBJ_ID__FOR__GRAPH__EMPTY
from osbot_utils.testing.__                                                             import __
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                       import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id


class test_Semantic_Graph__Utils(TestCase):                                             # Test semantic graph utilities

    @classmethod
    def setUpClass(cls):                                                                # Shared test objects (performance)
        cls.test_data = QA__Semantic_Graphs__Test_Data()
        cls.utils     = Semantic_Graph__Utils()

    def test__init__(self):                                                             # Test initialization
        with Semantic_Graph__Utils() as _:
            assert type(_) is Semantic_Graph__Utils

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_node(self):                                                           # Test node retrieval
        graph      = self.test_data.create_graph__simple_class()
        node_ids   = list(graph.nodes.keys())
        first_node = node_ids[0]
        found      = self.utils.get_node(graph, node_ids[0])
        not_found  = self.utils.get_node(graph, Node_Id(Obj_Id()))
        assert node_ids    == ['ff5bcf64', '02a4d1fa','53b63bbe']
        assert first_node  == "ff5bcf64"
        assert type(found) is Schema__Semantic_Graph__Node
        assert found.obj() == __(node_id_source = __(source_type = 'deterministic'        ,
                                                     seed        = 'test:node:my_module') ,
                                 node_id         = 'ff5bcf64'                              ,
                                 node_type       = 'module'                                ,
                                 name            = 'my_module'                             ,
                                 line_number     = 0                                       )

        assert not_found is None

    def test__has_node(self):                                                           # Test node existence check
        graph    = self.test_data.create_graph__simple_class()
        node_ids = list(graph.nodes.keys())

        assert self.utils.has_node(graph, node_ids[0])       is True
        assert self.utils.has_node(graph, Node_Id(Obj_Id())) is False

    def test__all_node_ids(self):                                                       # Test listing all node IDs
        graph = self.test_data.create_graph__simple_class()

        node_ids = self.utils.all_node_ids(graph)

        assert type(node_ids) is List__Node_Ids
        assert len(node_ids)  == 3                                                      # module, class, method

    def test__node_count(self):                                                         # Test node counting
        with self.test_data as _:
            graph = _.create_graph__empty()

            assert self.utils.node_count(graph) == 0

            node1 = _.create_node('class', 'A')
            graph.nodes[node1.node_id] = node1
            assert self.utils.node_count(graph) == 1

            node2 = _.create_node('class', 'B')
            graph.nodes[node2.node_id] = node2
            assert self.utils.node_count(graph) == 2

    def test__nodes_by_type(self):                                                      # Test filtering nodes by type
        with self.test_data as _:
            graph = _.create_graph__empty()

            node1 = _.create_node('class' , 'A')
            node2 = _.create_node('class' , 'B')
            node3 = _.create_node('method', 'foo')

            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2
            graph.nodes[node3.node_id] = node3

            classes = self.utils.nodes_by_type(graph, Node_Type_Ref('class'))
            methods = self.utils.nodes_by_type(graph, Node_Type_Ref('method'))
            unknown = self.utils.nodes_by_type(graph, Node_Type_Ref('unknown'))

            assert len(classes) == 2
            assert len(methods) == 1
            assert len(unknown) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__edge_count(self):                                                         # Test edge counting
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node('class', 'A')
            node2 = _.create_node('method', 'foo')
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2

            assert graph.graph_id               == OBJ_ID__FOR__GRAPH__EMPTY
            assert self.utils.edge_count(graph) == 0

            edge = _.create_edge(node1.node_id, 'has', node2.node_id)
            graph.edges.append(edge)
            assert self.utils.edge_count(graph) == 1

    def test__outgoing_edges(self):                                                     # Test outgoing edge lookup
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node('class', 'A')
            node2 = _.create_node('method', 'foo')
            node3 = _.create_node('method', 'bar')
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2
            graph.nodes[node3.node_id] = node3
    
            graph.edges.append(_.create_edge(node1.node_id, 'has', node2.node_id))
            graph.edges.append(_.create_edge(node1.node_id, 'has', node3.node_id))
    
            edges_from_node1 = self.utils.outgoing_edges(graph, node1.node_id)
            edges_from_node2 = self.utils.outgoing_edges(graph, node2.node_id)
    
            assert len(edges_from_node1) == 2
            assert len(edges_from_node2) == 0

    def test__incoming_edges(self):                                                     # Test incoming edge lookup
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node('class', 'A')
            node2 = _.create_node('class', 'B')
            node3 = _.create_node('method', 'foo')
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2
            graph.nodes[node3.node_id] = node3

            graph.edges.append(_.create_edge(node1.node_id, 'has', node3.node_id))
            graph.edges.append(_.create_edge(node2.node_id, 'has', node3.node_id))

            edges_to_node3 = self.utils.incoming_edges(graph, node3.node_id)
            edges_to_node1 = self.utils.incoming_edges(graph, node1.node_id)

            assert len(edges_to_node3) == 2
            assert len(edges_to_node1) == 0

    def test__edges_with_verb(self):                                                    # Test verb filtering
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node('class', 'A')
            node2 = _.create_node('method', 'foo')
            node3 = _.create_node('class', 'B')
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2
            graph.nodes[node3.node_id] = node3

            graph.edges.append(_.create_edge(node1.node_id, 'has', node2.node_id))
            graph.edges.append(_.create_edge(node1.node_id, 'inherits_from', node3.node_id))

            has_edges     = self.utils.edges_with_verb(graph, Safe_Str__Ontology__Verb('has'))
            inherit_edges = self.utils.edges_with_verb(graph, Safe_Str__Ontology__Verb('inherits_from'))
            calls_edges   = self.utils.edges_with_verb(graph, Safe_Str__Ontology__Verb('calls'))

        assert len(has_edges)     == 1
        assert len(inherit_edges) == 1
        assert len(calls_edges)   == 0

    def test__neighbors(self):                                                          # Test neighbor lookup
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node('class', 'A')
            node2 = _.create_node('method', 'foo')
            node3 = _.create_node('method', 'bar')
            node4 = _.create_node('class', 'B')
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2
            graph.nodes[node3.node_id] = node3
            graph.nodes[node4.node_id] = node4

            graph.edges.append(_.create_edge(node1.node_id, 'has', node2.node_id))
            graph.edges.append(_.create_edge(node1.node_id, 'has', node3.node_id))
            graph.edges.append(_.create_edge(node1.node_id, 'inherits_from', node4.node_id))

            all_neighbors = self.utils.neighbors(graph, node1.node_id)

            assert len(all_neighbors) == 3

    def test__has_edge(self):                                                           # Test edge existence check
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node('class', 'A')
            node2 = _.create_node('method', 'foo')
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2

            graph.edges.append(_.create_edge(node1.node_id, 'has', node2.node_id))

            has_edge   = self.utils.has_edge(graph, node1.node_id, Safe_Str__Ontology__Verb('has'), node2.node_id)
            no_reverse = self.utils.has_edge(graph, node2.node_id, Safe_Str__Ontology__Verb('has'), node1.node_id)
            no_verb    = self.utils.has_edge(graph, node1.node_id, Safe_Str__Ontology__Verb('calls'), node2.node_id)

            assert has_edge   is True
            assert no_reverse is False
            assert no_verb    is False

    def test__find_edge(self):                                                          # Test finding specific edge
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node('class', 'A')
            node2 = _.create_node('method', 'foo')
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2

            edge = _.create_edge(node1.node_id, 'has', node2.node_id)
            graph.edges.append(edge)

            found     = self.utils.find_edge(graph, node1.node_id, Safe_Str__Ontology__Verb('has'), node2.node_id)
            not_found = self.utils.find_edge(graph, node2.node_id, Safe_Str__Ontology__Verb('has'), node1.node_id)

            assert found       is not None
            assert type(found) is Schema__Semantic_Graph__Edge
            assert not_found   is None

    # ═══════════════════════════════════════════════════════════════════════════
    # QA Test Data Integration
    # ═══════════════════════════════════════════════════════════════════════════

    def test__qa_graph__node_count(self):                                               # Test counting QA graph
        graph = self.test_data.create_graph__simple_class()

        assert self.utils.node_count(graph) == 3

    def test__qa_graph__edge_count(self):                                               # Test counting QA graph edges
        graph = self.test_data.create_graph__simple_class()

        assert self.utils.edge_count(graph) == 2                                        # module→class, class→method

    def test__qa_graph__nodes_by_type(self):                                            # Test filtering QA graph
        graph = self.test_data.create_graph__simple_class()

        modules   = self.utils.nodes_by_type(graph, Node_Type_Ref('module'))
        classes   = self.utils.nodes_by_type(graph, Node_Type_Ref('class'))
        methods   = self.utils.nodes_by_type(graph, Node_Type_Ref('method'))
        functions = self.utils.nodes_by_type(graph, Node_Type_Ref('function'))

        assert len(modules)   == 1
        assert len(classes)   == 1
        assert len(methods)   == 1
        assert len(functions) == 0

    def test__empty_graph(self):                                                        # Test operations on empty graph
        graph = self.test_data.create_graph__empty()

        assert self.utils.node_count(graph)                                      == 0
        assert self.utils.edge_count(graph)                                      == 0
        assert len(self.utils.all_node_ids(graph))                               == 0
        assert self.utils.get_node(graph, Node_Id(Obj_Id()))                     is None
        assert self.utils.has_node(graph, Node_Id(Obj_Id()))                     is False
        assert len(self.utils.nodes_by_type(graph, Node_Type_Ref('class')))      == 0
        assert len(self.utils.neighbors(graph, Node_Id(Obj_Id())))               == 0