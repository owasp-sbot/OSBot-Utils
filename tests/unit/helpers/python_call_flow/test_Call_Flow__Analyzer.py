# ═══════════════════════════════════════════════════════════════════════════════
# test_Call_Flow__Analyzer - Tests for call flow analyzer
# ═══════════════════════════════════════════════════════════════════════════════

from unittest                                                                        import TestCase

from osbot_utils.utils.Objects                                                       import base_classes
from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe

from osbot_utils.helpers.python_call_flow.Call_Flow__Analyzer                        import Call_Flow__Analyzer
from osbot_utils.helpers.python_call_flow.Call_Flow__Builder                         import Call_Flow__Builder
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Config          import Schema__Call_Flow__Config
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Flow__Result          import Schema__Call_Flow__Result
from osbot_utils.helpers.python_call_flow.testing.QA__Call_Flow__Test_Data           import (QA__Call_Flow__Test_Data   ,
                                                                                             Sample__Simple_Class       ,
                                                                                             Sample__Self_Calls         ,
                                                                                             Sample__Multiple_Self_Calls,
                                                                                             Sample__Deep_Calls         ,
                                                                                             Sample__Recursive          ,
                                                                                             sample_standalone_function )


class test_Call_Flow__Analyzer(TestCase):                                            # Test analyzer class

    @classmethod
    def setUpClass(cls):                                                             # Shared setup - expensive operations
        cls.qa = QA__Call_Flow__Test_Data()

    def test__init__(self):                                                          # Test initialization
        with Call_Flow__Analyzer() as _:
            assert type(_)          is Call_Flow__Analyzer
            assert base_classes(_)  == [Type_Safe, object]
            assert type(_.config)   is Schema__Call_Flow__Config
            assert type(_.builder)  is Call_Flow__Builder

    def test__init__with_config(self):                                               # Test init with custom config
        config = Schema__Call_Flow__Config(max_depth=5, include_builtins=True)

        with Call_Flow__Analyzer(config=config) as _:
            assert _.config.max_depth        == 5
            assert _.config.include_builtins == True

    def test__analyze__simple_class(self):                                           # Test analyzing simple class
        with self.qa as _:
            result = _.create_result__simple_class()

            assert type(result)                is Schema__Call_Flow__Result
            assert result.total_nodes          >= 3                                  # class + 2 methods
            assert result.total_edges          >= 2                                  # contains edges
            assert 'Sample__Simple_Class'      in result.entry_point

    def test__analyze__self_calls(self):                                             # Test detecting self.method() calls
        with self.qa as _:
            result       = _.create_result__self_calls()
            calls_self_id = str(_.get_predicate_id__calls_self())

            self_call_count = _.count_edges_by_predicate(result, _.get_predicate_id__calls_self())

            assert result.total_nodes  == 3                                          # class + 2 methods
            assert self_call_count     >= 1                                          # do_work -> process

    def test__analyze__multiple_self_calls(self):                                    # Test multiple self calls
        with self.qa as _:
            result = _.create_result__multiple_self_calls()

            assert result.total_nodes  == 5                                          # class + 4 methods
            assert 'Sample__Multiple_Self_Calls' in result.entry_point

    def test__analyze__deep_calls(self):                                             # Test deep call chains
        with self.qa as _:
            result = _.create_result__deep_calls()

            assert result.total_nodes  == 5                                          # class + 4 level methods
            assert 'Sample__Deep_Calls' in result.entry_point

    def test__analyze__function(self):                                               # Test analyzing standalone function
        with self.qa as _:
            result = _.create_result__function()

            assert type(result)                    is Schema__Call_Flow__Result
            assert 'sample_standalone_function'    in result.entry_point
            assert result.total_nodes              >= 1

    def test__analyze__with_max_depth(self):                                         # Test max_depth config
        with self.qa as _:
            config = _.create_config__shallow()                                      # max_depth=1
            result = _.create_result__with_config(Sample__Deep_Calls, config)

            assert type(result) is Schema__Call_Flow__Result
            assert result.total_nodes >= 1                                           # At least class node

    def test__analyze__include_builtins(self):                                       # Test including builtins
        config = Schema__Call_Flow__Config(include_builtins=True)

        with Call_Flow__Analyzer(config=config) as analyzer:
            assert analyzer.config.include_builtins == True
            assert analyzer.should_skip_call('print') == False                       # Should NOT skip

    def test__analyze__exclude_builtins(self):                                       # Test excluding builtins
        config = Schema__Call_Flow__Config(include_builtins=False)

        with Call_Flow__Analyzer(config=config) as analyzer:
            assert analyzer.should_skip_call('print') == True                        # Should skip
            assert analyzer.should_skip_call('len')   == True

    def test__is_stdlib(self):                                                       # Test stdlib detection
        with Call_Flow__Analyzer() as _:
            assert _.is_stdlib('print')          == True
            assert _.is_stdlib('len')            == True
            assert _.is_stdlib('dict')           == True
            assert _.is_stdlib('my_custom_func') == False

    def test__should_skip_call(self):                                                # Test call skip logic
        config = Schema__Call_Flow__Config(include_builtins=False)

        with Call_Flow__Analyzer(config=config) as _:
            assert _.should_skip_call('print')   == True
            assert _.should_skip_call('my_func') == False

    def test__result__has_entry_point(self):                                         # Test result entry point
        with self.qa as _:
            result = _.create_result__self_calls()

            assert result.entry_point is not None
            assert 'Sample__Self_Calls' in result.entry_point

    def test__result__has_name_to_node_id(self):                                     # Test result name mapping
        with self.qa as _:
            result = _.create_result__self_calls()

            assert len(result.name_to_node_id) > 0
            found = any('Self_Calls' in k for k in result.name_to_node_id.keys())
            assert found

    def test__result__has_graph(self):                                               # Test result contains graph
        with self.qa as _:
            result = _.create_result__self_calls()

            assert result.graph       is not None
            assert result.total_nodes == len(list(result.graph.nodes.keys()))
            assert result.total_edges == len(result.graph.edges)

    def test__context_manager(self):                                                 # Test context manager pattern
        with Call_Flow__Analyzer() as analyzer:
            result = analyzer.analyze(Sample__Simple_Class)
            assert type(result) is Schema__Call_Flow__Result

    def test__all_sample_classes__analyzable(self):                                  # Test all samples can be analyzed
        with self.qa as _:
            for sample_class in _.get_all_sample_classes():
                with Call_Flow__Analyzer() as analyzer:
                    result = analyzer.analyze(sample_class)

                    assert result.total_nodes >= 1                                   # At least class node
                    assert sample_class.__name__ in result.entry_point


