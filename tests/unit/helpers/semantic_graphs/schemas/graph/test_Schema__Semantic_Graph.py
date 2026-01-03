from unittest                                                                        import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph        import Schema__Semantic_Graph
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge  import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node  import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id            import Node_Type_Id
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Ontology_Id             import Ontology_Id
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.testing.Graph__Deterministic__Ids                                   import graph_ids_for_tests
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id                   import Graph_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                    import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id

class test_Schema__Semantic_Graph(TestCase):                                         # Test semantic graph schema

    def create_node(self, node_type: str, name: str) -> Schema__Semantic_Graph__Node:
        return Schema__Semantic_Graph__Node(node_id   = Node_Id(Obj_Id())        ,
                                            node_type = Node_Type_Id(node_type)  ,
                                            name      = name                     )

    def create_edge(self, from_node: Node_Id, verb: str,
                    to_node: Node_Id) -> Schema__Semantic_Graph__Edge:
        return Schema__Semantic_Graph__Edge(
            edge_id   = Edge_Id(Obj_Id())                                            ,
            from_node = from_node                                                    ,
            verb      = Safe_Str__Ontology__Verb(verb)                               ,
            to_node   = to_node                                                      ,
        )

    def test__init__(self):                                                          # Test initialization
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id     = Graph_Id(Obj_Id())            ,
                                        ontology_ref = Ontology_Id('test')           ) as _:
                assert str(_.graph_id)     == 'a0000001'
                assert str(_.ontology_ref) == 'test'
                assert str(_.version)      == '1.0.0'
                assert _.node_count()      == 0
                assert _.edge_count()      == 0

    def test__add_node(self):                                                        # Test adding nodes
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id=Graph_Id(Obj_Id()), ontology_ref=Ontology_Id('test')) as _:
                node = self.create_node('class', 'MyClass')
                _.add_node(node)

                assert _.node_count() == 1
                assert _.get_node(str(node.node_id)) is node

    def test__add_node__fluent_api(self):                                            # Test fluent add_node returns graph
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id=Graph_Id(Obj_Id()), ontology_ref=Ontology_Id('test')) as _:
                result = _.add_node(self.create_node('class', 'A'))
                assert result is _                                                   # Returns self for chaining

    def test__add_edge(self):                                                        # Test adding edges
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id=Graph_Id(Obj_Id()), ontology_ref=Ontology_Id('test')) as _:
                node1 = self.create_node('class', 'A')
                node2 = self.create_node('method', 'foo')
                _.add_node(node1)
                _.add_node(node2)

                edge = self.create_edge(node1.node_id, 'has', node2.node_id)
                _.add_edge(edge)

                assert _.edge_count() == 1

    def test__get_node__returns_none_for_missing(self):                              # Test missing node lookup
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id=Graph_Id(Obj_Id()), ontology_ref=Ontology_Id('test')) as _:
                assert _.get_node('nonexistent') is None
                assert _.get_node('')            is None

    def test__nodes_by_type(self):                                                   # Test filtering by type
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id=Graph_Id(Obj_Id()), ontology_ref=Ontology_Id('test')) as _:
                _.add_node(self.create_node('class', 'A'))
                _.add_node(self.create_node('class', 'B'))
                _.add_node(self.create_node('method', 'foo'))
                _.add_node(self.create_node('method', 'bar'))
                _.add_node(self.create_node('function', 'helper'))

                classes   = _.nodes_by_type('class')
                methods   = _.nodes_by_type('method')
                functions = _.nodes_by_type('function')
                unknowns  = _.nodes_by_type('unknown')

                assert len(classes)   == 2
                assert len(methods)   == 2
                assert len(functions) == 1
                assert len(unknowns)  == 0

    def test__edges_from(self):                                                      # Test outgoing edge lookup
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id=Graph_Id(Obj_Id()), ontology_ref=Ontology_Id('test')) as _:
                node1 = self.create_node('class', 'A')
                node2 = self.create_node('method', 'foo')
                node3 = self.create_node('method', 'bar')
                _.add_node(node1).add_node(node2).add_node(node3)

                _.add_edge(self.create_edge(node1.node_id, 'has', node2.node_id))
                _.add_edge(self.create_edge(node1.node_id, 'has', node3.node_id))

                edges = _.edges_from(str(node1.node_id))
                assert len(edges) == 2

                empty = _.edges_from(str(node2.node_id))
                assert len(empty) == 0

    def test__edges_to(self):                                                        # Test incoming edge lookup
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id=Graph_Id(Obj_Id()), ontology_ref=Ontology_Id('test')) as _:
                node1 = self.create_node('class', 'A')
                node2 = self.create_node('class', 'B')
                node3 = self.create_node('method', 'foo')
                _.add_node(node1).add_node(node2).add_node(node3)

                _.add_edge(self.create_edge(node1.node_id, 'has', node3.node_id))
                _.add_edge(self.create_edge(node2.node_id, 'has', node3.node_id))

                edges = _.edges_to(str(node3.node_id))
                assert len(edges) == 2

                empty = _.edges_to(str(node1.node_id))
                assert len(empty) == 0

    def test__edges_by_verb(self):                                                   # Test verb filtering
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id=Graph_Id(Obj_Id()), ontology_ref=Ontology_Id('test')) as _:
                node1 = self.create_node('class', 'A')
                node2 = self.create_node('method', 'foo')
                node3 = self.create_node('class', 'B')
                _.add_node(node1).add_node(node2).add_node(node3)

                _.add_edge(self.create_edge(node1.node_id, 'has', node2.node_id))
                _.add_edge(self.create_edge(node1.node_id, 'inherits_from', node3.node_id))

                has_edges     = _.edges_by_verb('has')
                inherit_edges = _.edges_by_verb('inherits_from')
                calls_edges   = _.edges_by_verb('calls')

                assert len(has_edges)     == 1
                assert len(inherit_edges) == 1
                assert len(calls_edges)   == 0

    def test__neighbors(self):                                                       # Test neighbor lookup
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id=Graph_Id(Obj_Id()), ontology_ref=Ontology_Id('test')) as _:
                node1 = self.create_node('class', 'A')
                node2 = self.create_node('method', 'foo')
                node3 = self.create_node('method', 'bar')
                node4 = self.create_node('class', 'B')
                _.add_node(node1).add_node(node2).add_node(node3).add_node(node4)

                _.add_edge(self.create_edge(node1.node_id, 'has', node2.node_id))
                _.add_edge(self.create_edge(node1.node_id, 'has', node3.node_id))
                _.add_edge(self.create_edge(node1.node_id, 'inherits_from', node4.node_id))

                all_neighbors = _.neighbors(str(node1.node_id))
                assert len(all_neighbors) == 3

                has_neighbors = _.neighbors(str(node1.node_id), 'has')
                assert len(has_neighbors) == 2

                inherit_neighbors = _.neighbors(str(node1.node_id), 'inherits_from')
                assert len(inherit_neighbors) == 1

    def test__reverse_neighbors(self):                                               # Test reverse neighbor lookup
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id=Graph_Id(Obj_Id()), ontology_ref=Ontology_Id('test')) as _:
                node1 = self.create_node('class', 'A')
                node2 = self.create_node('class', 'B')
                node3 = self.create_node('method', 'foo')
                _.add_node(node1).add_node(node2).add_node(node3)

                _.add_edge(self.create_edge(node1.node_id, 'has', node3.node_id))
                _.add_edge(self.create_edge(node2.node_id, 'has', node3.node_id))

                reverse = _.reverse_neighbors(str(node3.node_id))
                assert len(reverse) == 2

                reverse_has = _.reverse_neighbors(str(node3.node_id), 'has')
                assert len(reverse_has) == 2

    def test__complex_graph(self):                                                   # Test realistic graph structure
        with graph_ids_for_tests():
            with Schema__Semantic_Graph(graph_id=Graph_Id(Obj_Id()), ontology_ref=Ontology_Id('code_structure')) as _:
                module    = self.create_node('module', 'my_module')                  # Build structure
                class_a   = self.create_node('class', 'ClassA')
                class_b   = self.create_node('class', 'ClassB')
                method_1  = self.create_node('method', 'method_one')
                method_2  = self.create_node('method', 'method_two')
                func      = self.create_node('function', 'helper')

                for n in [module, class_a, class_b, method_1, method_2, func]:
                    _.add_node(n)

                _.add_edge(self.create_edge(module.node_id, 'defines', class_a.node_id))
                _.add_edge(self.create_edge(module.node_id, 'defines', class_b.node_id))
                _.add_edge(self.create_edge(module.node_id, 'defines', func.node_id))
                _.add_edge(self.create_edge(class_a.node_id, 'has', method_1.node_id))
                _.add_edge(self.create_edge(class_a.node_id, 'has', method_2.node_id))
                _.add_edge(self.create_edge(class_a.node_id, 'inherits_from', class_b.node_id))

                assert _.node_count() == 6
                assert _.edge_count() == 6

                assert len(_.nodes_by_type('class'))    == 2                         # Verify structure
                assert len(_.nodes_by_type('method'))   == 2
                assert len(_.nodes_by_type('function')) == 1

                module_children = _.neighbors(str(module.node_id), 'defines')        # Module defines 3 things
                assert len(module_children) == 3

                class_a_methods = _.neighbors(str(class_a.node_id), 'has')           # ClassA has 2 methods
                assert len(class_a_methods) == 2

                class_a_parents = _.neighbors(str(class_a.node_id), 'inherits_from') # ClassA inherits from 1
                assert len(class_a_parents) == 1
