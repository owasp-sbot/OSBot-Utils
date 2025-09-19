import pytest
from typing                          import Type
from unittest                        import TestCase
from osbot_utils.type_safe.Type_Safe import Type_Safe


class test_Type_Safe__Step__Deserialize_Type(TestCase):

    def test__forward_ref_security(self):           # Ensure forward refs don't bypass security

        # This should work - Type_Safe subclass

        obj       = Safe_Forward_Ref()
        json_data = obj.json()
        restored   = Safe_Forward_Ref.from_json(json_data)  # Should work
        assert restored.json() == json_data

        obj          = Unsafe_Forward_Ref()
        obj.ref_type = Unsafe_Class                             # This should fail - arbitrary class
        json_data    = obj.json()

        with pytest.raises(ValueError, match="does not inherit from Type_Safe"):
            Unsafe_Forward_Ref.from_json(json_data)  # Should be blocked

# we need to define these classes here so that the deserialisation can find them

class Unsafe_Class:
    pass

class Unsafe_Forward_Ref(Type_Safe):
    ref_type: type

class Safe_Forward_Ref(Type_Safe):
    ref_type: Type['Safe_Forward_Ref']