from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Node_Type import Enum__Call_Graph__Node_Type


class test_Enum__Call_Graph__Node_Type(TestCase):                                    # Test node type enum

    def test__values(self):                                                          # Test all enum values exist
        assert Enum__Call_Graph__Node_Type.CLASS.value    == 'class'
        assert Enum__Call_Graph__Node_Type.METHOD.value   == 'method'
        assert Enum__Call_Graph__Node_Type.FUNCTION.value == 'function'
        assert Enum__Call_Graph__Node_Type.MODULE.value   == 'module'

    def test__from_string(self):                                                     # Test enum creation from string
        assert Enum__Call_Graph__Node_Type('class')    == Enum__Call_Graph__Node_Type.CLASS
        assert Enum__Call_Graph__Node_Type('method')   == Enum__Call_Graph__Node_Type.METHOD
        assert Enum__Call_Graph__Node_Type('function') == Enum__Call_Graph__Node_Type.FUNCTION
        assert Enum__Call_Graph__Node_Type('module')   == Enum__Call_Graph__Node_Type.MODULE

    def test__comparison(self):                                                      # Test enum comparison
        assert Enum__Call_Graph__Node_Type.CLASS    == 'class'
        assert Enum__Call_Graph__Node_Type.METHOD   == 'method'
        assert Enum__Call_Graph__Node_Type.FUNCTION == 'function'
        assert Enum__Call_Graph__Node_Type.MODULE   == 'module'
