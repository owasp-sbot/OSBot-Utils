from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph                import Schema__Call_Graph
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Edge          import Schema__Call_Graph__Edge
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Node          import Schema__Call_Graph__Node
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type import Enum__Call_Graph__Edge_Type
from osbot_utils.testing.Graph__Deterministic__Ids                                  import graph_ids_for_tests
from osbot_utils.testing.__                                                         import __
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                   import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Label  import Safe_Str__Label
from osbot_utils.type_safe.primitives.core.Safe_UInt                                import Safe_UInt


# todo: refactor out all methods from this class
class test_Schema__Call_Graph(TestCase):                                             # Test main graph schema

    def test__init__(self):                                                          # Test auto-initialization
        with Schema__Call_Graph() as _:
            assert len(_.nodes)           == 0                                       # Type_Safe__Dict behaves like dict
            assert len(_.edges)           == 0                                       # Type_Safe__List behaves like list
            assert _.node_count()         == 0
            assert _.edge_count()         == 0

    def test__add_node(self):                                                        # Test adding nodes
        with graph_ids_for_tests():
            with Schema__Call_Graph() as graph:
                node = Schema__Call_Graph__Node(node_id   = Node_Id(Obj_Id())         ,
                                                name      = Safe_Str__Label('func_a') )
                graph.add_node(node)
                assert graph.node_count()         == 1
                assert graph.get_node('c0000001') is node
                assert node.obj()                 == __(is_entry     = False      ,
                                                        is_external  = False      ,
                                                        is_recursive = False      ,
                                                        node_id      = 'c0000001' ,
                                                        name         = 'func_a'   ,
                                                        full_name    = ''         ,
                                                        node_type    = None       ,
                                                        module       = ''         ,
                                                        file_path    = ''         ,
                                                        depth        = 0          ,
                                                        calls        = []         ,
                                                        called_by    = []         ,
                                                        source_code  = ''         ,
                                                        line_number  = 0          )

    def test__add_edge(self):                                                        # Test adding edges
        with Schema__Call_Graph() as graph:
            edge = Schema__Call_Graph__Edge(edge_id   = Edge_Id() ,                  # without Obj_Id() in the contructor
                                            from_node = Node_Id() ,                  # this creates empty Edge_Id and Node_Ids
                                            to_node   = Node_Id() )
            graph.add_edge(edge)
            assert graph.edge_count() == 1

    def test__add_edge__with_edge_type(self):                                        # Test adding typed edges
        with graph_ids_for_tests():
            with Schema__Call_Graph() as graph:
                edge = Schema__Call_Graph__Edge(edge_id   = Edge_Id(Obj_Id())                     ,
                                                from_node = Node_Id(Obj_Id())                     ,
                                                to_node   = Node_Id(Obj_Id())                     ,
                                                edge_type = Enum__Call_Graph__Edge_Type.CONTAINS  )
                graph.add_edge(edge)

                assert graph.edge_count()       == 1
                assert graph.edges[0].edge_type == Enum__Call_Graph__Edge_Type.CONTAINS

    def test__get_node(self):                                                        # Test node retrieval
        with graph_ids_for_tests():
            with Schema__Call_Graph() as graph:
                node = Schema__Call_Graph__Node(node_id = Node_Id(Obj_Id())          ,
                                                name    = Safe_Str__Label('test')    )
                graph.add_node(node)

                assert graph.get_node('c0000001')    is node
                assert graph.get_node('nonexistent') is None

    def test__leaf_nodes(self):                                                      # Test finding leaf nodes
        with graph_ids_for_tests():
            with Schema__Call_Graph() as graph:
                node_a = Schema__Call_Graph__Node(node_id = Node_Id(Obj_Id())        ,
                                                  name    = Safe_Str__Label('a')     )
                node_b = Schema__Call_Graph__Node(node_id = Node_Id(Obj_Id())        ,
                                                  name    = Safe_Str__Label('b')     )
                node_a.calls.append(node_b.node_id)                                  # a calls b

                graph.add_node(node_a)
                graph.add_node(node_b)

                leaves = graph.leaf_nodes()
                assert len(leaves)    == 1
                assert leaves[0].name == 'b'                                         # b has no outgoing calls

    def test__root_nodes(self):                                                      # Test finding root nodes
        with graph_ids_for_tests():
            with Schema__Call_Graph() as graph:
                node_a = Schema__Call_Graph__Node(node_id = Node_Id(Obj_Id())        ,
                                                  name    = Safe_Str__Label('a')     )
                node_b = Schema__Call_Graph__Node(node_id = Node_Id(Obj_Id())        ,
                                                  name    = Safe_Str__Label('b')     )
                node_b.called_by.append(node_a.node_id)                              # b is called by a

                graph.add_node(node_a)
                graph.add_node(node_b)

                roots = graph.root_nodes()
                assert len(roots)    == 1
                assert roots[0].name == 'a'                                          # a has no incoming calls

    def test__nodes_at_depth(self):                                                  # Test depth filtering
        with graph_ids_for_tests():
            with Schema__Call_Graph() as graph:
                node_0  = Schema__Call_Graph__Node(node_id = Node_Id(Obj_Id())       ,
                                                   name    = Safe_Str__Label('root') ,
                                                   depth   = Safe_UInt(0)            )
                node_1a = Schema__Call_Graph__Node(node_id = Node_Id(Obj_Id())       ,
                                                   name    = Safe_Str__Label('a')    ,
                                                   depth   = Safe_UInt(1)            )
                node_1b = Schema__Call_Graph__Node(node_id = Node_Id(Obj_Id())       ,
                                                   name    = Safe_Str__Label('b')    ,
                                                   depth   = Safe_UInt(1)            )
                node_2  = Schema__Call_Graph__Node(node_id = Node_Id(Obj_Id())       ,
                                                   name    = Safe_Str__Label('deep') ,
                                                   depth   = Safe_UInt(2)            )

                graph.add_node(node_0)
                graph.add_node(node_1a)
                graph.add_node(node_1b)
                graph.add_node(node_2)

                assert len(graph.nodes_at_depth(0)) == 1
                assert len(graph.nodes_at_depth(1)) == 2
                assert len(graph.nodes_at_depth(2)) == 1
                assert len(graph.nodes_at_depth(3)) == 0
