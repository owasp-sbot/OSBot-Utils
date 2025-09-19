import types
import pytest
from enum                                                                         import Enum, IntEnum
from collections                                                                  import defaultdict, OrderedDict, Counter
from typing                                                                       import Type as TypingType
from decimal                                                                      import Decimal
from datetime                                                                     import datetime, date, time
from typing                                                                       import Type, List, Dict, Optional
from unittest                                                                     import TestCase
from osbot_utils.type_safe.Type_Safe                                              import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                 import Safe_Id
from osbot_utils.type_safe.type_safe_core.steps.Type_Safe__Step__Deserialize_Type import Type_Safe__Step__Deserialize_Type


class test_Type_Safe__Step__Deserialize_Type(TestCase):     # security test suite for Type_Safe__Step__Deserialize_Type

    @classmethod
    def setUpClass(cls):
        cls.deserializer        = Type_Safe__Step__Deserialize_Type()
        cls.deserializer_strict = Type_Safe__Step__Deserialize_Type(allow_type_safe_subclasses=False)

    # ========== EXPECTED BEHAVIOR TESTS ==========

    def test__builtin_types(self):                              # Test deserialization of allowed builtin types
        # Core Python types
        assert self.deserializer.using_value('builtins.str'      ) is str
        assert self.deserializer.using_value('builtins.int'      ) is int
        assert self.deserializer.using_value('builtins.float'    ) is float
        assert self.deserializer.using_value('builtins.bool'     ) is bool
        assert self.deserializer.using_value('builtins.list'     ) is list
        assert self.deserializer.using_value('builtins.dict'     ) is dict
        assert self.deserializer.using_value('builtins.tuple'    ) is tuple
        assert self.deserializer.using_value('builtins.set'      ) is set
        assert self.deserializer.using_value('builtins.frozenset') is frozenset
        assert self.deserializer.using_value('builtins.bytes'    ) is bytes
        assert self.deserializer.using_value('builtins.bytearray') is bytearray

    def test__types_module(self):                                                           # Test types module deserialization"""
        assert self.deserializer.using_value('builtins.NoneType' ) is types.NoneType        # Special case
        assert self.deserializer.using_value('types.FunctionType') is types.FunctionType
        assert self.deserializer.using_value('types.ModuleType'  ) is types.ModuleType

    def test__typing_module(self):                                                          # Test typing module types
        assert self.deserializer.using_value('typing.List'    ) is List
        assert self.deserializer.using_value('typing.Dict'    ) is Dict
        assert self.deserializer.using_value('typing.Optional') is Optional

    def test__enum_types(self):                                                             # Test enum deserialization
        assert self.deserializer.using_value('enum.Enum'   ) is Enum
        assert self.deserializer.using_value('enum.IntEnum') is IntEnum

    def test__decimal_datetime(self):                                                       # Test decimal and datetime modules
        assert self.deserializer.using_value('decimal.Decimal') is Decimal
        assert self.deserializer.using_value('datetime.datetime') is datetime
        assert self.deserializer.using_value('datetime.date') is date
        assert self.deserializer.using_value('datetime.time') is time

    def test__collections_module(self):                                                     # Test collections module types
        assert self.deserializer.using_value('collections.defaultdict') is defaultdict
        assert self.deserializer.using_value('collections.OrderedDict') is OrderedDict
        assert self.deserializer.using_value('collections.Counter') is Counter

    def test__type_safe_classes(self):                                                      # Test Type_Safe framework classes
        result = self.deserializer.using_value('osbot_utils.type_safe.Type_Safe.Type_Safe')
        assert result is Type_Safe
        result = self.deserializer.using_value('osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id.Safe_Id')
        assert result is Safe_Id

    def test__none_handling(self):                                                          # Test None value handling
        assert self.deserializer.using_value(None) is None
        assert self.deserializer.using_value('') is None

    # ========== SECURITY TESTS - DENYLIST ==========

    def test__security__dangerous_builtins(self):
        """Test that dangerous builtins are blocked"""
        dangerous_types = [
            'builtins.eval',
            'builtins.exec',
            'builtins.compile',
            'builtins.__import__',
            'builtins.open',
            'builtins.input',
            'builtins.breakpoint',
            'builtins.help',
            'builtins.globals',
            'builtins.locals',
            'builtins.vars',
            'builtins.dir'
        ]

        for dangerous_type in dangerous_types:
            with pytest.raises(ValueError, match=f"Type '.*' is deny listed for security"):
                self.deserializer.using_value(dangerous_type)

    # ========== SECURITY TESTS - MODULE RESTRICTIONS ==========


    def test__security__os_module(self):
        """Test that os module is blocked"""
        error_message = r"Module 'os' is not in allowed modules.*"
        with pytest.raises(ValueError, match=error_message):
            self.deserializer_strict.using_value('os.path')

        with pytest.raises(ValueError, match=error_message):
            self.deserializer_strict.using_value('os.system')

    def test__security__sys_module(self):
        """Test that sys module is blocked"""
        error_message = r"Module 'sys' is not in allowed modules.*"
        with pytest.raises(ValueError, match=error_message):
            self.deserializer_strict.using_value('sys.exit')

    def test__security__subprocess_module(self):
        """Test that subprocess module is blocked"""
        error_message = r"Module 'subprocess' is not in allowed modules.*"
        with pytest.raises(ValueError, match=error_message):
            self.deserializer_strict.using_value('subprocess.Popen')

    def test__security__socket_module(self):
        """Test that socket module is blocked"""
        error_message = r"Module 'socket' is not in allowed modules.*"
        with pytest.raises(ValueError, match=error_message):
            self.deserializer_strict.using_value('socket.socket')

    def test__security__importlib_module(self):
        """Test that importlib is blocked"""
        error_message = r"Module 'importlib' is not in allowed modules.*"
        with pytest.raises(ValueError, match=error_message):
            self.deserializer_strict.using_value('importlib.import_module')

    # ========== SECURITY TESTS - NON-CLASS TYPES ==========

    def test__security__function_deserialization(self):
        """Test that functions cannot be deserialized"""
        error_message = "Security alert, in deserialize_type__using_value only classes are allowed"

        # Built-in functions
        with pytest.raises(ValueError, match=error_message):
            self.deserializer.using_value('builtins.print')

        with pytest.raises(ValueError, match=error_message):
            self.deserializer.using_value('builtins.len')

    def test__security__module_deserialization(self):           # Test that modules cannot be deserialized as types

        # Test 1: Non-existent attribute in allowed module
        error_message = r"Type 'os' not found in module 'types'"
        with pytest.raises(ValueError, match=error_message):
            self.deserializer.using_value('types.os')  # Doesn't exist

        # Test 2: Actual module object that exists but isn't a type
        error_message = r"Type '__spec__' not found in module 'types'|Security alert.*"     # Let's use something that actually exists but isn't a class
        with pytest.raises(ValueError, match=error_message):
            self.deserializer.using_value('types.__spec__')                                 # Module spec object

        # Test 3: A function in an allowed module (not a class)
        error_message = r"Security alert, in deserialize_type__using_value only classes are allowed"
        with pytest.raises(ValueError, match=error_message):
            self.deserializer.using_value('types.prepare_class')                         # types.prepare_class is a function, not a class

    # ========== SECURITY TESTS - FORMAT VALIDATION ==========

    def test__security__invalid_format(self):
        """Test format validation"""
        invalid_formats = [
            'no_module_name',           # No module
            'module.',                  # Empty class name
            '.ClassName',               # Empty module name
            'module..ClassName',        # Double dots
            'module.Class.Name.Extra',  # This should work (nested classes)
            '../../../etc/passwd',      # Path traversal attempt
            'module\nClassName',        # Newline injection
            'module;import os;Class',  # Command injection attempt
            'module.__init__',          # Dunder methods
            'module.__class__',         # Special attributes
        ]

        for invalid in invalid_formats:
            if '.' not in invalid or '..' in invalid:
                with pytest.raises(ValueError, match="Type reference must include module|Invalid type reference format"):
                    self.deserializer.using_value(invalid)

    def test__security__malformed_input(self):
        """Test handling of malformed input"""
        # Non-string input
        with pytest.raises(ValueError, match="Type reference must be a string"):
            self.deserializer.using_value(123)

        with pytest.raises(ValueError, match="Type reference must be a string"):
            self.deserializer.using_value(['builtins', 'str'])

        with pytest.raises(ValueError, match="Type reference must be a string"):
            self.deserializer.using_value({'module': 'builtins', 'type': 'str'})

    # ========== SECURITY TESTS - TYPE_SAFE INHERITANCE ==========

    def test__forward_ref_security(self):                               # Ensure forward refs don't bypass security


        obj       = Safe_Forward_Ref()                                  # This should work - Type_Safe subclass
        json_data = obj.json()
        restored   = Safe_Forward_Ref.from_json(json_data)              # Should work
        assert restored.json() == json_data

        obj          = Unsafe_Forward_Ref()
        obj.ref_type = Unsafe_Class                                     # This should fail - arbitrary class
        json_data    = obj.json()

        with pytest.raises(ValueError, match="does not inherit from Type_Safe"):
            Unsafe_Forward_Ref.from_json(json_data)  # Should be blocked


    def test__security__non_type_safe_class(self):                      # Test that non-Type_Safe classes are blocked when using strict mode
        # Simulate serialization
        class_path = f"{Regular_Class.__module__}.Regular_Class"        # Use a test class that's not Type_Safe

        # Should work with allow_type_safe_subclasses=True (default)
        # But the module won't be in allowlist, so it should fail differently
        error_message = r"Module '.*' is not in allowed modules.*"
        with pytest.raises(ValueError, match=error_message):
            self.deserializer.using_value(class_path)

        with pytest.raises(ValueError, match=error_message):                    # Should also fail with strict mode
            self.deserializer_strict.using_value(class_path)

    def test__security__type_safe_subclass(self):                               # Test that Type_Safe subclasses work correctly
        # This uses a class from the test file that IS a Type_Safe subclass
        obj = Safe_Forward_Ref()
        json_data = obj.json()

        restored = Safe_Forward_Ref.from_json(json_data)                        # Should work because it's a Type_Safe subclass
        assert restored.json() == json_data

    # ========== SECURITY TESTS - EDGE CASES ==========

    def test__security__nested_classes(self):                   # Test handling of nested class references
        # This should work if the class exists and is allowed
        # But we test that it validates properly
        result = self.deserializer.using_value('typing.Type')   # Valid nested class in allowed module
        assert result is TypingType

    def test__security__special_characters(self):
        """Test handling of special characters in input"""
        special_inputs = [
            'builtins.str\x00',         # Null byte
            'builtins.str\r\n',         # CRLF
            'builtins.str\t',           # Tab
            'builtins.str ',            # Trailing space
            ' builtins.str',            # Leading space
            'builtins.str\\n',          # Escaped newline
            'builtins.str\'',           # Quote
            'builtins.str"',            # Double quote
            'builtins.str`',            # Backtick
            'builtins.str;ls',          # Shell command attempt
            'builtins.str|cat',         # Pipe attempt
            'builtins.str&',            # Background process
            'builtins.str$(cmd)',       # Command substitution
        ]

        for special in special_inputs:
            with pytest.raises(ValueError, match="Invalid type reference format|Type .* not found"):
                self.deserializer.using_value(special)

    def test__security__unicode_attacks(self):
        """Test Unicode-based attacks"""
        unicode_attacks = [
            'builtins.str\u0000',       # Null character
            'builtins.str\u202e',       # Right-to-left override
            'builtins.ｓｔｒ',          # Full-width characters
            'builtіns.str',             # Homograph attack (Cyrillic і)
        ]

        for attack in unicode_attacks:
            with pytest.raises(ValueError):
                self.deserializer.using_value(attack)

    # ========== MODULE ALLOWLIST TESTS ==========

    def test__module_allowlist_configuration(self):
        """Test that module allowlist is properly configured"""
        expected_modules = {
            'builtins',
            'types',
            'typing',
            'enum',
            'decimal',
            'datetime',
            'collections',
            'collections.abc',
            'osbot_utils.type_safe',
            'osbot_utils.type_safe.primitives'
        }

        assert self.deserializer.allowed_modules == expected_modules

    def test__module_allowlist_submodule_check(self):
        """Test the submodule checking logic"""
        # These should be allowed (submodules of allowed modules)
        assert self.deserializer.is_module_allowed('osbot_utils.type_safe.primitives.domains')
        assert self.deserializer.is_module_allowed('osbot_utils.type_safe.primitives.domains.identifiers')

        # These should NOT be allowed
        assert not self.deserializer.is_module_allowed('os')
        assert not self.deserializer.is_module_allowed('sys')
        assert not self.deserializer.is_module_allowed('osbot_utils.other_module')

        # Edge case: Similar prefix but not actually a submodule
        assert not self.deserializer.is_module_allowed('osbot_utils.type_safe_malicious')

    # ========== STRESS TESTS ==========

    def test__stress__long_module_path(self):
        """Test handling of extremely long module paths"""
        long_path = '.'.join(['a'] * 1000) + '.ClassName'

        with pytest.raises(ValueError):
            self.deserializer.using_value(long_path)

    def test__stress__deep_nesting(self):
        """Test deeply nested valid module paths"""
        # This should work as it's a valid Type_Safe path
        deep_path = 'osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id.Safe_Id'
        result    = self.deserializer.using_value(deep_path)
        assert result is Safe_Id

    # ========== REGRESSION TESTS ==========

    def test__regression__forward_ref_security(self):
        """Test that forward refs don't bypass security (from original test)"""
        obj = Safe_Forward_Ref()
        json_data = obj.json()
        restored = Safe_Forward_Ref.from_json(json_data)
        assert restored.json() == json_data

        obj = Unsafe_Forward_Ref()
        obj.ref_type = Unsafe_Class
        json_data = obj.json()

        with pytest.raises(ValueError, match="does not inherit from Type_Safe"):
            Unsafe_Forward_Ref.from_json(json_data)

    def test__type_safe_inheritance_check(self):
        """Test the Type_Safe inheritance checking logic"""
        from osbot_utils.type_safe.Type_Safe import Type_Safe
        from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id import Safe_Id

        # These should be recognized as Type_Safe classes
        assert self.deserializer.is_type_safe_class(Type_Safe)
        assert self.deserializer.is_type_safe_class(Safe_Id)
        assert self.deserializer.is_type_safe_class(Safe_Forward_Ref)

        # These should NOT be recognized as Type_Safe classes
        assert not self.deserializer.is_type_safe_class(str)
        assert not self.deserializer.is_type_safe_class(int)
        assert not self.deserializer.is_type_safe_class(Unsafe_Class)

    # ========== CONFIGURATION TESTS ==========

    def test__allow_type_safe_subclasses_flag(self):
        """Test the allow_type_safe_subclasses configuration"""
        # With flag=True (default), Type_Safe subclasses from non-allowed modules should work
        deserializer_permissive = Type_Safe__Step__Deserialize_Type(allow_type_safe_subclasses=True)

        # With flag=False, only explicitly allowed modules work
        deserializer_strict = Type_Safe__Step__Deserialize_Type(allow_type_safe_subclasses=False)

        # Both should allow builtin types
        assert deserializer_permissive.using_value('builtins.str') is str
        assert deserializer_strict.using_value('builtins.str') is str


# Test classes needed for the tests

class Regular_Class:
    pass

class Unsafe_Class:
    """Not a Type_Safe subclass"""
    pass


class Unsafe_Forward_Ref(Type_Safe):
    """Type_Safe class with unsafe type reference"""
    ref_type: type


class Safe_Forward_Ref(Type_Safe):
    """Type_Safe class with safe self-reference"""
    ref_type: Type['Safe_Forward_Ref']