from unittest                                                                        import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Node  import Schema__Semantic_Graph__Node
from osbot_utils.helpers.semantic_graphs.schemas.identifier.Node_Type_Id            import Node_Type_Id
from osbot_utils.testing.Graph__Deterministic__Ids                                   import graph_ids_for_tests
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id


class test_Schema__Semantic_Graph__Node(TestCase):                                   # Test semantic graph node schema

    def test__init__(self):                                                          # Test initialization
        with graph_ids_for_tests():
            with Schema__Semantic_Graph__Node(node_id   = Node_Id(Obj_Id())          ,
                                              node_type = Node_Type_Id('class')      ,
                                              name      = 'MyClass'                  ) as _:
                assert str(_.node_id)     == 'c0000001'
                assert str(_.node_type)   == 'class'
                assert str(_.name)        == 'MyClass'
                assert int(_.line_number) == 0                                       # Default
