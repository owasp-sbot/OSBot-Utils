from unittest                                                                       import TestCase
from osbot_utils.helpers.python_call_flow.schemas.enums.Enum__Call_Graph__Edge_Type import Enum__Call_Graph__Edge_Type


class test_Enum__Call_Graph__Edge_Type(TestCase):                                    # Test edge type enum

    def test__values(self):                                                          # Test all enum values exist
        assert Enum__Call_Graph__Edge_Type.CONTAINS.value == 'contains'
        assert Enum__Call_Graph__Edge_Type.CALLS.value    == 'calls'
        assert Enum__Call_Graph__Edge_Type.SELF.value     == 'self'
        assert Enum__Call_Graph__Edge_Type.CHAIN.value    == 'chain'

    def test__from_string(self):                                                     # Test enum creation from string
        assert Enum__Call_Graph__Edge_Type('contains') == Enum__Call_Graph__Edge_Type.CONTAINS
        assert Enum__Call_Graph__Edge_Type('calls')    == Enum__Call_Graph__Edge_Type.CALLS
        assert Enum__Call_Graph__Edge_Type('self')     == Enum__Call_Graph__Edge_Type.SELF
        assert Enum__Call_Graph__Edge_Type('chain')    == Enum__Call_Graph__Edge_Type.CHAIN

    def test__comparison(self):                                                      # Test enum comparison
        assert Enum__Call_Graph__Edge_Type.CONTAINS == 'contains'
        assert Enum__Call_Graph__Edge_Type.CALLS    == 'calls'
        assert Enum__Call_Graph__Edge_Type.SELF     == 'self'
        assert Enum__Call_Graph__Edge_Type.CHAIN    == 'chain'
