from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.Call_Flow__Node__Registry                 import Call_Flow__Node__Registry
from osbot_utils.testing.Graph__Deterministic__Ids                                  import graph_ids_for_tests
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                   import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict               import Type_Safe__Dict


class Sample__Target:                                                                # Sample class for testing
    def sample_method(self):
        pass


def sample_function():                                                               # Sample function for testing
    pass


class test_Call_Flow__Node__Registry(TestCase):                                      # Test node registry

    def test__init__(self):                                                          # Test initialization
        with Call_Flow__Node__Registry() as _:
            assert type(_.name_to_node_id) is Type_Safe__Dict
            assert len(_.name_to_node_id)  == 0

    def test__register_and_lookup(self):                                             # Test register and lookup
        with graph_ids_for_tests():
            with Call_Flow__Node__Registry() as _:
                node_id = Node_Id(Obj_Id())
                _.register('test.name', node_id)

                assert _.lookup('test.name')     == node_id
                assert _.lookup('nonexistent')   is None

    def test__exists(self):                                                          # Test exists check
        with graph_ids_for_tests():
            with Call_Flow__Node__Registry() as _:
                node_id = Node_Id(Obj_Id())
                _.register('test.name', node_id)

                assert _.exists('test.name')   is True
                assert _.exists('nonexistent') is False

    def test__reset(self):                                                           # Test reset clears registry
        with graph_ids_for_tests():
            with Call_Flow__Node__Registry() as _:
                _.register('test.name', Node_Id(Obj_Id()))
                assert len(_.name_to_node_id) == 1

                _.reset()
                assert len(_.name_to_node_id) == 0

    def test__qualified_name__class(self):                                           # Test qualified name for class
        with Call_Flow__Node__Registry() as _:
            name = _.qualified_name(Sample__Target)
            assert 'Sample__Target' in name
            assert '.' in name                                                       # Has module prefix

    def test__qualified_name__function(self):                                        # Test qualified name for function
        with Call_Flow__Node__Registry() as _:
            name = _.qualified_name(sample_function)
            assert 'sample_function' in name

    def test__short_name(self):                                                      # Test short name extraction
        with Call_Flow__Node__Registry() as _:
            assert _.short_name(Sample__Target)  == 'Sample__Target'
            assert _.short_name(sample_function) == 'sample_function'

    def test__module_name(self):                                                     # Test module name extraction
        with Call_Flow__Node__Registry() as _:
            module = _.module_name(Sample__Target)
            assert 'test_Call_Flow__Node__Registry' in module

    def test__file_path(self):                                                       # Test file path extraction
        with Call_Flow__Node__Registry() as _:
            path = _.file_path(Sample__Target)
            assert path.endswith('.py')

    def test__line_number(self):                                                     # Test line number extraction
        with Call_Flow__Node__Registry() as _:
            line = _.line_number(Sample__Target)
            assert line > 0
