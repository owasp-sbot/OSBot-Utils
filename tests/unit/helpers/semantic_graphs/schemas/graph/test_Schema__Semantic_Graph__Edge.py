from unittest                                                                        import TestCase
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph__Edge  import Schema__Semantic_Graph__Edge
from osbot_utils.helpers.semantic_graphs.schemas.safe_str.Safe_Str__Ontology__Verb   import Safe_Str__Ontology__Verb
from osbot_utils.testing.Graph__Deterministic__Ids                                   import graph_ids_for_tests
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                    import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                    import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                     import Obj_Id




class test_Schema__Semantic_Graph__Edge(TestCase):                                   # Test semantic graph edge schema

    def test__init__(self):                                                          # Test initialization
        with graph_ids_for_tests():
            with Schema__Semantic_Graph__Edge(edge_id   = Edge_Id(Obj_Id())          ,
                                              from_node = Node_Id(Obj_Id())          ,
                                              verb      = Safe_Str__Ontology__Verb('has'),
                                              to_node   = Node_Id(Obj_Id())          ) as _:
                assert str(_.edge_id)     == 'e0000001'
                assert str(_.from_node)   == 'c0000001'
                assert str(_.verb)        == 'has'
                assert str(_.to_node)     == 'c0000002'
                assert int(_.line_number) == 0                                       # Default
