# ═══════════════════════════════════════════════════════════════════════════════
# test_Schema__Call_Flow__Result - Tests for result schema
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase

from osbot_utils.utils.Objects                                                       import base_classes
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.helpers.semantic_graphs.schemas.graph.Schema__Semantic_Graph        import Schema__Semantic_Graph

from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Result          import Schema__Call_Flow__Result
from osbot_utils.helpers.python_call_flow.testing.QA__Call_Flow__Test_Data           import QA__Call_Flow__Test_Data


class test_Schema__Call_Flow__Result(TestCase):                                      # Test result schema

    @classmethod
    def setUpClass(cls):
        cls.qa = QA__Call_Flow__Test_Data()

    def test__init__(self):                                                          # Test initialization
        with Schema__Call_Flow__Result() as _:
            assert type(_)                is Schema__Call_Flow__Result
            assert base_classes(_)        == [Type_Safe, object]
            assert type(_.graph)          is Schema__Semantic_Graph
            assert _.entry_point          == ''
            assert _.total_nodes          == 0
            assert _.total_edges          == 0
            assert _.max_depth_reached    == 0
            assert len(_.name_to_node_id) == 0

    def test__with_values(self):                                                     # Test with explicit values
        graph = Schema__Semantic_Graph()

        with Schema__Call_Flow__Result(graph            = graph            ,
                                       entry_point      = 'test.MyClass'   ,
                                       total_nodes      = 5                ,
                                       total_edges      = 4                ,
                                       max_depth_reached = 3               ) as _:
            assert _.graph             is graph
            assert _.entry_point       == 'test.MyClass'
            assert _.total_nodes       == 5
            assert _.total_edges       == 4
            assert _.max_depth_reached == 3

    def test__from_analyzer(self):                                                   # Test result from analyzer
        with self.qa as _:
            result = _.create_result__self_calls()

            assert type(result)                is Schema__Call_Flow__Result
            assert type(result.graph)          is Schema__Semantic_Graph
            assert 'Sample__Self_Calls'        in result.entry_point
            assert result.total_nodes          == 3                                  # class + 2 methods
            assert result.total_edges          >= 2                                  # contains + self-call
            assert len(result.name_to_node_id) >= 3

    def test__name_to_node_id__mapping(self):                                        # Test name to node ID mapping
        with self.qa as _:
            result = _.create_result__simple_class()

            assert len(result.name_to_node_id) >= 3                                  # class + 2 methods

            # Verify keys contain expected names
            keys = list(result.name_to_node_id.keys())
            found_class  = any('Simple_Class' in k for k in keys)
            found_method = any('method_a' in k or 'method_b' in k for k in keys)

            assert found_class
            assert found_method

    def test__graph__contains_nodes(self):                                           # Test graph has nodes
        with self.qa as _:
            result = _.create_result__self_calls()

            assert len(list(result.graph.nodes.keys())) == result.total_nodes

    def test__graph__contains_edges(self):                                           # Test graph has edges
        with self.qa as _:
            result = _.create_result__self_calls()

            assert len(result.graph.edges) == result.total_edges

    def test__max_depth_reached(self):                                               # Test max depth tracking
        with self.qa as _:
            result = _.create_result__deep_calls()

            assert result.max_depth_reached >= 1                                     # At least some depth

    def test__all_fixtures__have_valid_results(self):                                # Test all QA fixtures produce valid results
        with self.qa as _:
            all_fixtures = _.create_all_fixtures()

            for name, fixture in all_fixtures.items():
                result = fixture['result']

                assert type(result)       is Schema__Call_Flow__Result
                assert result.entry_point != ''
                assert result.total_nodes >= 1
                assert result.graph       is not None