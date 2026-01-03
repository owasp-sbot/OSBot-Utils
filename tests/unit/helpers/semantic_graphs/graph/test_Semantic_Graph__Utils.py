# ═══════════════════════════════════════════════════════════════════════════════
# Test Semantic_Graph__Utils - Tests for semantic graph utility operations
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase
from osbot_utils.helpers.semantic_graphs.graph.Semantic_Graph__Utils                 import Semantic_Graph__Utils
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph        import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node  import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge  import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id             import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id              import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.testing.Graph__Deterministic__Ids                                   import graph_ids_for_tests
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                   import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                    import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id


class test_Semantic_Graph__Utils(TestCase):                                          # Test semantic graph utilities

    @classmethod
    def setUpClass(cls):                                                             # Create shared test objects
        cls.utils = Semantic_Graph__Utils()

    def create_test_graph(self) -> Schema__Semantic_Graph:                           # Helper to create test graph
        return Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id()),
                                      ontology_ref = Ontology_Id('test'))

    def create_node(self, node_type: str, name: str) -> Schema__Semantic_Graph__Node:
        return Schema__Semantic_Graph__Node(node_id   = Node_Id(Obj_Id()),
                                            node_type = Node_Type_Id(node_type),
                                            name      = name                   )

    def create_edge(self, from_node: Node_Id, verb: str,
                    to_node: Node_Id) -> Schema__Semantic_Graph__Edge:
        return Schema__Semantic_Graph__Edge(edge_id   = Edge_Id(Obj_Id()),
                                            from_node = from_node         ,
                                            verb      = Safe_Str__Ontology__Verb(verb),
                                            to_node   = to_node           )

    def test__init__(self):                                                          # Test initialization
        with Semantic_Graph__Utils() as _:
            assert type(_) is Semantic_Graph__Utils

    def test__add_node(self):                                                        # Test adding nodes to graph
        with graph_ids_for_tests():
            graph = self.create_test_graph()
            node  = self.create_node('class', 'MyClass')

            result = self.utils.add_node(graph, node)

            assert result is graph                                                   # Returns graph for chaining
            assert self.utils.node_count(graph) == 1
            assert self.utils.get_node(graph, node.node_id) is node

    def test__get_node(self):                                                        # Test node retrieval
        with graph_ids_for_tests():
            graph = self.create_test_graph()
            node  = self.create_node('class', 'MyClass')
            self.utils.add_node(graph, node)

            found    = self.utils.get_node(graph, node.node_id)
            not_found = self.utils.get_node(graph, 'nonexistent')

            assert found     is node
            assert not_found is None

    def test__node_count(self):                                                      # Test node counting
        with graph_ids_for_tests():
            graph = self.create_test_graph()

            assert self.utils.node_count(graph) == 0

            self.utils.add_node(graph, self.create_node('class', 'A'))
            assert self.utils.node_count(graph) == 1

            self.utils.add_node(graph, self.create_node('class', 'B'))
            assert self.utils.node_count(graph) == 2

    def test__nodes_by_type(self):                                                   # Test filtering nodes by type
        with graph_ids_for_tests():
            graph = self.create_test_graph()
            self.utils.add_node(graph, self.create_node('class', 'A'))
            self.utils.add_node(graph, self.create_node('class', 'B'))
            self.utils.add_node(graph, self.create_node('method', 'foo'))

            classes = self.utils.nodes_by_type(graph, 'class')
            methods = self.utils.nodes_by_type(graph, 'method')
            unknown = self.utils.nodes_by_type(graph, 'unknown')

            assert len(classes) == 2
            assert len(methods) == 1
            assert len(unknown) == 0

    def test__add_edge(self):                                                        # Test adding edges to graph
        with graph_ids_for_tests():
            graph = self.create_test_graph()
            node1 = self.create_node('class', 'A')
            node2 = self.create_node('method', 'foo')
            self.utils.add_node(graph, node1)
            self.utils.add_node(graph, node2)

            edge   = self.create_edge(node1.node_id, 'has', node2.node_id)
            result = self.utils.add_edge(graph, edge)

            assert result is graph                                                   # Returns graph for chaining
            assert self.utils.edge_count(graph) == 1

    def test__edge_count(self):                                                      # Test edge counting
        with graph_ids_for_tests():
            graph = self.create_test_graph()
            node1 = self.create_node('class', 'A')
            node2 = self.create_node('method', 'foo')
            self.utils.add_node(graph, node1)
            self.utils.add_node(graph, node2)

            assert self.utils.edge_count(graph) == 0

            self.utils.add_edge(graph, self.create_edge(node1.node_id, 'has', node2.node_id))
            assert self.utils.edge_count(graph) == 1

    def test__edges_from(self):                                                      # Test outgoing edge lookup
        with graph_ids_for_tests():
            graph = self.create_test_graph()
            node1 = self.create_node('class', 'A')
            node2 = self.create_node('method', 'foo')
            node3 = self.create_node('method', 'bar')
            self.utils.add_node(graph, node1)
            self.utils.add_node(graph, node2)
            self.utils.add_node(graph, node3)

            self.utils.add_edge(graph, self.create_edge(node1.node_id, 'has', node2.node_id))
            self.utils.add_edge(graph, self.create_edge(node1.node_id, 'has', node3.node_id))

            edges_from_node1 = self.utils.edges_from(graph, node1.node_id)
            edges_from_node2 = self.utils.edges_from(graph, node2.node_id)

            assert len(edges_from_node1) == 2
            assert len(edges_from_node2) == 0

    def test__edges_to(self):                                                        # Test incoming edge lookup
        with graph_ids_for_tests():
            graph = self.create_test_graph()
            node1 = self.create_node('class', 'A')
            node2 = self.create_node('class', 'B')
            node3 = self.create_node('method', 'foo')
            self.utils.add_node(graph, node1)
            self.utils.add_node(graph, node2)
            self.utils.add_node(graph, node3)

            self.utils.add_edge(graph, self.create_edge(node1.node_id, 'has', node3.node_id))
            self.utils.add_edge(graph, self.create_edge(node2.node_id, 'has', node3.node_id))

            edges_to_node3 = self.utils.edges_to(graph, node3.node_id)
            edges_to_node1 = self.utils.edges_to(graph, node1.node_id)

            assert len(edges_to_node3) == 2
            assert len(edges_to_node1) == 0

    def test__edges_by_verb(self):                                                   # Test verb filtering
        with graph_ids_for_tests():
            graph = self.create_test_graph()
            node1 = self.create_node('class', 'A')
            node2 = self.create_node('method', 'foo')
            node3 = self.create_node('class', 'B')
            self.utils.add_node(graph, node1)
            self.utils.add_node(graph, node2)
            self.utils.add_node(graph, node3)

            self.utils.add_edge(graph, self.create_edge(node1.node_id, 'has', node2.node_id))
            self.utils.add_edge(graph, self.create_edge(node1.node_id, 'inherits_from', node3.node_id))

            has_edges     = self.utils.edges_by_verb(graph, 'has')
            inherit_edges = self.utils.edges_by_verb(graph, 'inherits_from')
            calls_edges   = self.utils.edges_by_verb(graph, 'calls')

            assert len(has_edges)     == 1
            assert len(inherit_edges) == 1
            assert len(calls_edges)   == 0

    def test__neighbors(self):                                                       # Test neighbor lookup
        with graph_ids_for_tests():
            graph = self.create_test_graph()
            node1 = self.create_node('class', 'A')
            node2 = self.create_node('method', 'foo')
            node3 = self.create_node('method', 'bar')
            node4 = self.create_node('class', 'B')
            self.utils.add_node(graph, node1)
            self.utils.add_node(graph, node2)
            self.utils.add_node(graph, node3)
            self.utils.add_node(graph, node4)

            self.utils.add_edge(graph, self.create_edge(node1.node_id, 'has', node2.node_id))
            self.utils.add_edge(graph, self.create_edge(node1.node_id, 'has', node3.node_id))
            self.utils.add_edge(graph, self.create_edge(node1.node_id, 'inherits_from', node4.node_id))

            all_neighbors     = self.utils.neighbors(graph, node1.node_id)
            has_neighbors     = self.utils.neighbors(graph, node1.node_id, 'has')
            inherit_neighbors = self.utils.neighbors(graph, node1.node_id, 'inherits_from')

            assert len(all_neighbors)     == 3
            assert len(has_neighbors)     == 2
            assert len(inherit_neighbors) == 1

    def test__reverse_neighbors(self):                                               # Test reverse neighbor lookup
        with graph_ids_for_tests():
            graph = self.create_test_graph()
            node1 = self.create_node('class', 'A')
            node2 = self.create_node('class', 'B')
            node3 = self.create_node('method', 'foo')
            self.utils.add_node(graph, node1)
            self.utils.add_node(graph, node2)
            self.utils.add_node(graph, node3)

            self.utils.add_edge(graph, self.create_edge(node1.node_id, 'has', node3.node_id))
            self.utils.add_edge(graph, self.create_edge(node2.node_id, 'has', node3.node_id))

            reverse     = self.utils.reverse_neighbors(graph, node3.node_id)
            reverse_has = self.utils.reverse_neighbors(graph, node3.node_id, 'has')

            assert len(reverse)     == 2
            assert len(reverse_has) == 2