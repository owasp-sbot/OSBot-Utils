from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.Call_Flow__Node__Factory                  import Call_Flow__Node__Factory
from osbot_utils.helpers.python_call_flow.Call_Flow__Node__Registry                 import Call_Flow__Node__Registry
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Config        import Schema__Call_Graph__Config
from osbot_utils.helpers.python_call_flow.schemas.Schema__Call_Graph__Node          import Schema__Call_Graph__Node
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Node_Type import Enum__Call_Graph__Node_Type


class Sample__Class:                                                                 # Sample class for testing
    def sample_method(self):
        pass


def sample_function():                                                               # Sample function for testing
    pass


class test_Call_Flow__Node__Factory(TestCase):                                       # Test node factory

    @classmethod
    def setUpClass(cls):                                                             # Shared setup
        cls.factory  = Call_Flow__Node__Factory()
        cls.registry = Call_Flow__Node__Registry()
        cls.factory.registry = cls.registry
        cls.factory.config   = Schema__Call_Graph__Config()

    def test__init__(self):                                                          # Test initialization
        with Call_Flow__Node__Factory() as _:
            assert type(_.config)   is Schema__Call_Graph__Config
            assert type(_.registry) is Call_Flow__Node__Registry

    def test__create_class_node(self):                                               # Test class node creation
        node = self.factory.create_class_node(Sample__Class, depth=0)

        assert type(node)       is Schema__Call_Graph__Node
        assert node.node_type   == Enum__Call_Graph__Node_Type.CLASS
        assert str(node.name)   == 'Sample__Class'
        assert int(node.depth)  == 0
        assert node.is_external is False

    def test__create_method_node(self):                                              # Test method node creation
        method = Sample__Class.sample_method
        node   = self.factory.create_method_node(method, depth=1, is_method=True)

        assert type(node)      is Schema__Call_Graph__Node
        assert node.node_type  == Enum__Call_Graph__Node_Type.METHOD
        assert str(node.name)  == 'sample_method'
        assert int(node.depth) == 1

    def test__create_function_node(self):                                            # Test function node creation
        node = self.factory.create_function_node(sample_function, depth=0)

        assert type(node)      is Schema__Call_Graph__Node
        assert node.node_type  == Enum__Call_Graph__Node_Type.FUNCTION
        assert str(node.name)  == 'sample_function'
        assert int(node.depth) == 0

    def test__create_external_node(self):                                            # Test external node creation
        node = self.factory.create_external_node('some.external.call', depth=2)

        assert type(node)       is Schema__Call_Graph__Node
        assert node.node_type   == Enum__Call_Graph__Node_Type.FUNCTION
        assert str(node.name)   == 'call'                                            # Short name
        assert int(node.depth)  == 2
        assert node.is_external is True

    def test__create_class_node__has_metadata(self):                                 # Test class node has file/line info
        node = self.factory.create_class_node(Sample__Class, depth=0)

        assert str(node.file_path).endswith('.py')
        assert int(node.line_number) > 0
        assert 'Sample__Class' in str(node.full_name)
