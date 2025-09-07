import pytest
from unittest                                                      import TestCase
from osbot_utils.type_safe.Type_Safe                               import Type_Safe
from osbot_utils.type_safe.primitives.safe_str.llm.Enum__LLM__Role import Enum__LLM__Role


class test_Enum__LLM__Role(TestCase):
    
    def test_enum_values(self):                                            # Test all enum values
        assert Enum__LLM__Role.SYSTEM.value    == 'system'
        assert Enum__LLM__Role.USER.value      == 'user'
        assert Enum__LLM__Role.ASSISTANT.value == 'assistant'
        assert Enum__LLM__Role.TOOL.value      == 'tool'
        
        # Enum members are strings
        assert str(Enum__LLM__Role.SYSTEM)     == 'system'
        assert str(Enum__LLM__Role.USER)       == 'user'
        assert str(Enum__LLM__Role.ASSISTANT)  == 'assistant'
        assert str(Enum__LLM__Role.TOOL)       == 'tool'

        assert repr(Enum__LLM__Role.SYSTEM)    == "<Enum__LLM__Role.SYSTEM: 'system'>"
        assert repr(Enum__LLM__Role.USER)      == "<Enum__LLM__Role.USER: 'user'>"
        assert repr(Enum__LLM__Role.ASSISTANT) == "<Enum__LLM__Role.ASSISTANT: 'assistant'>"
        assert repr(Enum__LLM__Role.TOOL)      == "<Enum__LLM__Role.TOOL: 'tool'>"

        assert f"Role: {Enum__LLM__Role.SYSTEM}"    == "Role: system"
        assert f"Role: {Enum__LLM__Role.USER}"      == "Role: user"
        assert f"Role: {Enum__LLM__Role.ASSISTANT}" == "Role: assistant"
        assert f"Role: {Enum__LLM__Role.TOOL}"      == "Role: tool"

    def test_string_compatibility(self):                                   # Test str inheritance
        # Direct string comparison
        assert Enum__LLM__Role.USER   == 'user'
        assert Enum__LLM__Role.SYSTEM == 'system'
        
        # Can be used as strings
        role = Enum__LLM__Role.ASSISTANT
        assert f"Role: {role}"  == "Role: assistant"
        assert role + "_suffix" == "assistant_suffix"
    
    def test_enum_creation_from_string(self):                             # Test creating enum from string
        # Valid values
        assert Enum__LLM__Role('system')    == Enum__LLM__Role.SYSTEM
        assert Enum__LLM__Role('user')      == Enum__LLM__Role.USER
        assert Enum__LLM__Role('assistant') == Enum__LLM__Role.ASSISTANT
        assert Enum__LLM__Role('tool')      == Enum__LLM__Role.TOOL
        
        # Invalid values raise error
        with pytest.raises(ValueError, match="'invalid' is not a valid Enum__LLM__Role"):
            Enum__LLM__Role('invalid')
        
        with pytest.raises(ValueError, match="'SYSTEM' is not a valid Enum__LLM__Role"):
            Enum__LLM__Role('SYSTEM')  # Case sensitive
    
    def test_enum_iteration(self):                                        # Test iterating over enum values
        roles = list(Enum__LLM__Role)
        assert len(roles) == 4
        assert Enum__LLM__Role.SYSTEM    in roles
        assert Enum__LLM__Role.USER      in roles
        assert Enum__LLM__Role.ASSISTANT in roles
        assert Enum__LLM__Role.TOOL      in roles
        
        # Get all values
        values = [role.value for role in Enum__LLM__Role]
        assert values == ['system', 'user', 'assistant', 'tool']
    
    def test_enum_membership(self):                                       # Test membership checks
        assert 'user' in [r.value for r in Enum__LLM__Role]
        assert 'invalid' not in [r.value for r in Enum__LLM__Role]
        
        # Check if a string is a valid role
        def is_valid_role(value):
            try:
                Enum__LLM__Role(value)
                return True
            except ValueError:
                return False
        
        assert is_valid_role('user'     ) is True
        assert is_valid_role('system'   ) is True
        assert is_valid_role('invalid'  ) is False
        assert is_valid_role('USER'     ) is False  # Case sensitive
    
    def test_usage_in_type_safe(self):                                    # Test integration with Type_Safe
        class Schema__LLM__Message(Type_Safe):
            role    : Enum__LLM__Role
            content : str
        
        with Schema__LLM__Message() as _:
            # Auto-initialization (enum fields don't auto-init to a value)
            assert _.role is None  # Enums default to None if not set
            assert _.content == ''
            
            # String auto-converts to enum
            _.role = 'user'
            assert type(_.role) is Enum__LLM__Role
            assert _.role == Enum__LLM__Role.USER
            assert _.role == 'user'
            
            # Direct enum assignment
            _.role = Enum__LLM__Role.ASSISTANT
            assert _.role == 'assistant'
            
            # Invalid role raises error
            with pytest.raises(ValueError):
                _.role = 'invalid_role'
    
    def test_json_serialization(self):                                    # Test JSON round-trip
        class Schema__Conversation(Type_Safe):
            role    : Enum__LLM__Role
            message : str
        
        with Schema__Conversation() as original:
            original.role = Enum__LLM__Role.SYSTEM
            original.message = 'You are a helpful assistant.'
            
            # Serialize - enum becomes string
            json_data = original.json()
            assert json_data == { 'role': 'system',
                                  'message': 'You are a helpful assistant.'}
            assert type(json_data['role']) is str
            
            # Deserialize - string becomes enum
            with Schema__Conversation.from_json(json_data) as restored:
                assert type(restored.role) is Enum__LLM__Role
                assert restored.role == Enum__LLM__Role.SYSTEM
                assert restored.role == 'system'
                assert restored.message == original.message
    
    def test_switch_statement_pattern(self):                              # Test using enum in match/switch
        def process_message(role: Enum__LLM__Role, content: str):
            if role == Enum__LLM__Role.SYSTEM:
                return f"System: {content}"
            elif role == Enum__LLM__Role.USER:
                return f"User says: {content}"
            elif role == Enum__LLM__Role.ASSISTANT:
                return f"AI responds: {content}"
            elif role == Enum__LLM__Role.TOOL:
                return f"Tool output: {content}"
            else:
                return f"Unknown role: {content}"
        
        assert process_message(Enum__LLM__Role.USER, "Hello") == "User says: Hello"
        assert process_message(Enum__LLM__Role.ASSISTANT, "Hi") == "AI responds: Hi"
    
    def test_enum_comparison(self):                                       # Test enum comparisons
        role1 = Enum__LLM__Role.USER
        role2 = Enum__LLM__Role.USER
        role3 = Enum__LLM__Role.ASSISTANT
        
        # Same enum values are equal
        assert role1 == role2
        assert role1 is Enum__LLM__Role.USER
        
        # Different enum values are not equal
        assert role1 != role3
        assert role1 is not role3
        
        # Can compare with strings
        assert role1 == 'user'
        assert role1 != 'assistant'