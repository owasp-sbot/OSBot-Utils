# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic_Graph__Utils - Tests for semantic graph utility operations
# Uses QA__Semantic_Graphs__Test_Data for consistent test data creation
#
# Updated for Brief 3.8:
#   - Uses node_type_id instead of node_type ref
#   - Uses predicate_id instead of verb
#   - Uses from_node_id/to_node_id instead of from_node/to_node
#   - Added property query methods
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                           import TestCase
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Utils                    import Semantic_Graph__Utils
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Node_Properties       import Dict__Node_Properties
from osbot_utils.helpers.semantic_graphs.schemas.collection.Dict__Edge_Properties       import Dict__Edge_Properties
from osbot_utils.helpers.semantic_graphs.schemas.collection.List__Node_Ids              import List__Node_Ids
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge     import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node     import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id                import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Predicate_Id                import Predicate_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Property_Name_Id            import Property_Name_Id
from osbot_utils.helpers.semantic_graphs.testing.QA__Semantic_Graphs__Test_Data         import QA__Semantic_Graphs__Test_Data
from osbot_utils.testing.__                                                             import __
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text            import Safe_Str__Text
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                       import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                        import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id         import Safe_Str__Id


class test_Semantic_Graph__Utils(TestCase):                                             # Test semantic graph utilities

    @classmethod
    def setUpClass(cls):                                                                # Shared test objects (performance)
        cls.test_data = QA__Semantic_Graphs__Test_Data()
        cls.utils     = Semantic_Graph__Utils()

        # Cache commonly used IDs (Brief 3.8 API)
        cls.class_type_id    = cls.test_data.get_node_type_id__class()
        cls.method_type_id   = cls.test_data.get_node_type_id__method()
        cls.contains_pred_id = cls.test_data.get_predicate_id__contains()
        cls.calls_pred_id    = cls.test_data.get_predicate_id__calls()

        # Property IDs for Brief 3.8
        cls.line_number_id   = cls.test_data.get_property_name_id__line_number()
        cls.call_count_id    = cls.test_data.get_property_name_id__call_count()

    def test__init__(self):                                                             # Test initialization
        with Semantic_Graph__Utils() as _:
            assert type(_) is Semantic_Graph__Utils

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_node(self):                                                           # Test node retrieval
        builder    = self.test_data.create_graph_with_properties()
        graph      = builder.build()
        node_ids   = list(graph.nodes.keys())
        first_id   = node_ids[0]
        found      = self.utils.get_node(graph, first_id)
        not_found  = self.utils.get_node(graph, Node_Id(Obj_Id()))

        assert type(found) is Schema__Semantic_Graph__Node
        assert found       is not None
        assert not_found   is None

    def test__has_node(self):                                                           # Test node existence check
        builder  = self.test_data.create_graph_with_properties()
        graph    = builder.build()
        node_ids = list(graph.nodes.keys())

        assert self.utils.has_node(graph, node_ids[0])       is True
        assert self.utils.has_node(graph, Node_Id(Obj_Id())) is False

    def test__all_node_ids(self):                                                       # Test listing all node IDs
        builder = self.test_data.create_graph_with_properties()
        graph   = builder.build()

        node_ids = self.utils.all_node_ids(graph)

        assert type(node_ids) is List__Node_Ids
        assert len(node_ids)  == 4                                                      # module, class, method, function

    def test__node_count(self):                                                         # Test node counting
        with self.test_data as _:
            graph = _.create_graph__empty()

            assert self.utils.node_count(graph) == 0

            node1 = _.create_node(self.class_type_id, Safe_Str__Id('A'))
            graph.nodes[node1.node_id] = node1
            assert self.utils.node_count(graph) == 1

            node2 = _.create_node(self.class_type_id, Safe_Str__Id('B'))
            graph.nodes[node2.node_id] = node2
            assert self.utils.node_count(graph) == 2

    def test__nodes_by_type(self):                                                      # Test filtering nodes by type
        with self.test_data as _:
            graph = _.create_graph__empty()

            node1 = _.create_node(self.class_type_id , Safe_Str__Id('A'))
            node2 = _.create_node(self.class_type_id , Safe_Str__Id('B'))
            node3 = _.create_node(self.method_type_id, Safe_Str__Id('foo'))

            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2
            graph.nodes[node3.node_id] = node3

            classes = self.utils.nodes_by_type(graph, self.class_type_id)
            methods = self.utils.nodes_by_type(graph, self.method_type_id)
            unknown = self.utils.nodes_by_type(graph, Node_Type_Id(Obj_Id()))

            assert len(classes) == 2
            assert len(methods) == 1
            assert len(unknown) == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Node Property Operations (Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_node_property(self):                                                  # Test getting node property
        builder = self.test_data.create_graph_with_properties()
        graph   = builder.build()

        node_with_prop = None                                                           # Find node with line_number
        for node in graph.nodes.values():
            if node.properties and self.line_number_id in node.properties:
                node_with_prop = node
                break

        assert node_with_prop is not None
        value = self.utils.get_node_property(graph, node_with_prop.node_id, self.line_number_id)
        assert value is not None
        assert type(value) is Safe_Str__Text

    def test__has_node_property(self):                                                  # Test checking node property exists
        builder = self.test_data.create_graph_with_properties()
        graph   = builder.build()

        node_with_prop = None
        for node in graph.nodes.values():
            if node.properties and self.line_number_id in node.properties:
                node_with_prop = node
                break

        assert node_with_prop is not None
        assert self.utils.has_node_property(graph, node_with_prop.node_id, self.line_number_id)   is True
        assert self.utils.has_node_property(graph, node_with_prop.node_id, Property_Name_Id(Obj_Id())) is False

    def test__nodes_with_property(self):                                                # Test finding nodes with specific property
        builder = self.test_data.create_graph_with_properties()
        graph   = builder.build()

        nodes_with_line_number = self.utils.nodes_with_property(graph, self.line_number_id)
        nodes_with_unknown     = self.utils.nodes_with_property(graph, Property_Name_Id(Obj_Id()))

        assert len(nodes_with_line_number) >= 1                                         # At least one has line_number
        assert len(nodes_with_unknown)     == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Operations
    # ═══════════════════════════════════════════════════════════════════════════

    def test__edge_count(self):                                                         # Test edge counting
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node(self.class_type_id, Safe_Str__Id('A'))
            node2 = _.create_node(self.method_type_id, Safe_Str__Id('foo'))
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2

            assert self.utils.edge_count(graph) == 0

            edge = _.create_edge(node1.node_id, self.contains_pred_id, node2.node_id)
            graph.edges.append(edge)
            assert self.utils.edge_count(graph) == 1

    def test__outgoing_edges(self):                                                     # Test outgoing edge lookup
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node(self.class_type_id, Safe_Str__Id('A'))
            node2 = _.create_node(self.method_type_id, Safe_Str__Id('foo'))
            node3 = _.create_node(self.method_type_id, Safe_Str__Id('bar'))
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2
            graph.nodes[node3.node_id] = node3

            graph.edges.append(_.create_edge(node1.node_id, self.contains_pred_id, node2.node_id))
            graph.edges.append(_.create_edge(node1.node_id, self.contains_pred_id, node3.node_id))

            edges_from_node1 = self.utils.outgoing_edges(graph, node1.node_id)
            edges_from_node2 = self.utils.outgoing_edges(graph, node2.node_id)

            assert len(edges_from_node1) == 2
            assert len(edges_from_node2) == 0

    def test__incoming_edges(self):                                                     # Test incoming edge lookup
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node(self.class_type_id, Safe_Str__Id('A'))
            node2 = _.create_node(self.class_type_id, Safe_Str__Id('B'))
            node3 = _.create_node(self.method_type_id, Safe_Str__Id('foo'))
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2
            graph.nodes[node3.node_id] = node3

            graph.edges.append(_.create_edge(node1.node_id, self.contains_pred_id, node3.node_id))
            graph.edges.append(_.create_edge(node2.node_id, self.contains_pred_id, node3.node_id))

            edges_to_node3 = self.utils.incoming_edges(graph, node3.node_id)
            edges_to_node1 = self.utils.incoming_edges(graph, node1.node_id)

            assert len(edges_to_node3) == 2
            assert len(edges_to_node1) == 0

    def test__edges_with_predicate(self):                                               # Test predicate filtering
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node(self.class_type_id, Safe_Str__Id('A'))
            node2 = _.create_node(self.method_type_id, Safe_Str__Id('foo'))
            node3 = _.create_node(self.method_type_id, Safe_Str__Id('bar'))
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2
            graph.nodes[node3.node_id] = node3

            graph.edges.append(_.create_edge(node1.node_id, self.contains_pred_id, node2.node_id))
            graph.edges.append(_.create_edge(node2.node_id, self.calls_pred_id   , node3.node_id))

            contains_edges = self.utils.edges_with_predicate(graph, self.contains_pred_id)
            calls_edges    = self.utils.edges_with_predicate(graph, self.calls_pred_id)
            unknown_edges  = self.utils.edges_with_predicate(graph, Predicate_Id(Obj_Id()))

        assert len(contains_edges) == 1
        assert len(calls_edges)    == 1
        assert len(unknown_edges)  == 0

    def test__neighbors(self):                                                          # Test neighbor lookup
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node(self.class_type_id, Safe_Str__Id('A'))
            node2 = _.create_node(self.method_type_id, Safe_Str__Id('foo'))
            node3 = _.create_node(self.method_type_id, Safe_Str__Id('bar'))
            node4 = _.create_node(self.class_type_id, Safe_Str__Id('B'))
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2
            graph.nodes[node3.node_id] = node3
            graph.nodes[node4.node_id] = node4

            graph.edges.append(_.create_edge(node1.node_id, self.contains_pred_id, node2.node_id))
            graph.edges.append(_.create_edge(node1.node_id, self.contains_pred_id, node3.node_id))
            graph.edges.append(_.create_edge(node1.node_id, self.contains_pred_id, node4.node_id))

            all_neighbors = self.utils.neighbors(graph, node1.node_id)

            assert len(all_neighbors) == 3

    def test__has_edge(self):                                                           # Test edge existence check
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node(self.class_type_id, Safe_Str__Id('A'))
            node2 = _.create_node(self.method_type_id, Safe_Str__Id('foo'))
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2

            graph.edges.append(_.create_edge(node1.node_id, self.contains_pred_id, node2.node_id))

            has_edge   = self.utils.has_edge(graph, node1.node_id, self.contains_pred_id, node2.node_id)
            no_reverse = self.utils.has_edge(graph, node2.node_id, self.contains_pred_id, node1.node_id)
            no_pred    = self.utils.has_edge(graph, node1.node_id, self.calls_pred_id   , node2.node_id)

            assert has_edge   is True
            assert no_reverse is False
            assert no_pred    is False

    def test__find_edge(self):                                                          # Test finding specific edge
        with self.test_data as _:
            graph = _.create_graph__empty()
            node1 = _.create_node(self.class_type_id, Safe_Str__Id('A'))
            node2 = _.create_node(self.method_type_id, Safe_Str__Id('foo'))
            graph.nodes[node1.node_id] = node1
            graph.nodes[node2.node_id] = node2

            edge = _.create_edge(node1.node_id, self.contains_pred_id, node2.node_id)
            graph.edges.append(edge)

            found     = self.utils.find_edge(graph, node1.node_id, self.contains_pred_id, node2.node_id)
            not_found = self.utils.find_edge(graph, node2.node_id, self.contains_pred_id, node1.node_id)

            assert found       is not None
            assert type(found) is Schema__Semantic_Graph__Edge
            assert not_found   is None

    # ═══════════════════════════════════════════════════════════════════════════
    # Edge Property Operations (Brief 3.8)
    # ═══════════════════════════════════════════════════════════════════════════

    def test__get_edge_property(self):                                                  # Test getting edge property
        builder = self.test_data.create_graph_with_properties()
        graph   = builder.build()

        edge_with_prop = None                                                           # Find edge with call_count
        for edge in graph.edges:
            if edge.properties and self.call_count_id in edge.properties:
                edge_with_prop = edge
                break

        assert edge_with_prop is not None
        value = self.utils.get_edge_property(edge_with_prop, self.call_count_id)
        assert value is not None
        assert type(value) is Safe_Str__Text

    def test__has_edge_property(self):                                                  # Test checking edge property exists
        builder = self.test_data.create_graph_with_properties()
        graph   = builder.build()

        edge_with_prop = None
        for edge in graph.edges:
            if edge.properties and self.call_count_id in edge.properties:
                edge_with_prop = edge
                break

        assert edge_with_prop is not None
        assert self.utils.has_edge_property(edge_with_prop, self.call_count_id)   is True
        assert self.utils.has_edge_property(edge_with_prop, Property_Name_Id(Obj_Id())) is False

    def test__edges_with_property(self):                                                # Test finding edges with specific property
        builder = self.test_data.create_graph_with_properties()
        graph   = builder.build()

        edges_with_call_count = self.utils.edges_with_property(graph, self.call_count_id)
        edges_with_unknown    = self.utils.edges_with_property(graph, Property_Name_Id(Obj_Id()))

        assert len(edges_with_call_count) >= 1                                          # At least one has call_count
        assert len(edges_with_unknown)    == 0

    # ═══════════════════════════════════════════════════════════════════════════
    # QA Test Data Integration
    # ═══════════════════════════════════════════════════════════════════════════

    def test__qa_graph__node_count(self):                                               # Test counting QA graph
        builder = self.test_data.create_graph_with_properties()
        graph   = builder.build()

        assert self.utils.node_count(graph) == 4                                        # module, class, method, function

    def test__qa_graph__edge_count(self):                                               # Test counting QA graph edges
        builder = self.test_data.create_graph_with_properties()
        graph   = builder.build()

        assert self.utils.edge_count(graph) == 4                                        # contains x3, calls x1

    def test__qa_graph__nodes_by_type(self):                                            # Test filtering QA graph
        builder = self.test_data.create_graph_with_properties()
        graph   = builder.build()

        classes = self.utils.nodes_by_type(graph, self.class_type_id)
        methods = self.utils.nodes_by_type(graph, self.method_type_id)

        assert len(classes) >= 1
        assert len(methods) >= 1

    def test__empty_graph(self):                                                        # Test operations on empty graph
        graph = self.test_data.create_graph__empty()

        assert self.utils.node_count(graph)                                    == 0
        assert self.utils.edge_count(graph)                                    == 0
        assert len(self.utils.all_node_ids(graph))                             == 0
        assert self.utils.get_node(graph, Node_Id(Obj_Id()))                   is None
        assert self.utils.has_node(graph, Node_Id(Obj_Id()))                   is False
        assert len(self.utils.nodes_by_type(graph, self.class_type_id))        == 0
        assert len(self.utils.neighbors(graph, Node_Id(Obj_Id())))             == 0