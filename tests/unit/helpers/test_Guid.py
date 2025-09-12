from unittest                 import TestCase
from osbot_utils.type_safe.primitives.domains.identifiers.Guid import Guid


class test_Guid(TestCase):
    def setUp(self):
        self.test_value = "test-guid"
        self.guid = Guid(self.test_value)

    def test_create_guid(self):
        assert isinstance(self.guid, Guid)
        assert isinstance(self.guid, str)
        assert len(str(self.guid)) == 36                                                # Standard UUID length

    def test_deterministic(self):
        guid_1 = Guid(self.test_value)
        guid_2 = Guid(self.test_value)
        assert guid_1    == guid_2                                                      # Same input produces same UUID
        assert guid_1    == '2d68e4f3-bb56-5e6f-a2a6-9c20e650f08a'
        assert Guid('a') == '8a809dc1-0090-52e4-bf96-c888f7e20aa5'                      # static strings always produce the same value
        assert Guid('b') == '6e2adca9-5cbe-5d1b-bd74-3ed29cf04fc3'

    def test_different_inputs(self):
        guid_1 = Guid("value-1")
        guid_2 = Guid("value-2")
        assert guid_1 != guid_2                                                         # Different inputs produce different UUIDs

    def test_empty_input(self):
        guid = Guid("")                                                                 # Empty string is valid
        assert isinstance(guid, Guid)
        assert len(str(guid)) == 36

    def test_none_input(self):
        with self.assertRaises(ValueError) as context:
            Guid(None)  # Non-string input
        assert "value provided was not a string" in str(context.exception)

    def test_invalid_input(self):
        with self.assertRaises(ValueError) as context:
            Guid(123)                                                                   # Non-string input
        assert "value provided was not a string" in str(context.exception)
