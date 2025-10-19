import re
import json
import pytest

from osbot_utils.testing.__                                 import __
from osbot_utils.utils.Objects                              import base_types
from unittest                                               import TestCase
from osbot_utils.type_safe.primitives.core.Safe_Str         import Safe_Str, TYPE_SAFE__STR__MAX_LENGTH
from osbot_utils.type_safe.Type_Safe                        import Type_Safe
from osbot_utils.type_safe.Type_Safe__Primitive             import Type_Safe__Primitive



class test_Safe_Str(TestCase):

    def test_Safe_Str_class(self):
        # Valid cases - only alphanumerics allowed in base class
        assert str(Safe_Str('aaaabbb'   )) == 'aaaabbb'
        assert str(Safe_Str('AAA123bbb' )) == 'AAA123bbb'
        assert str(Safe_Str('123start'  )) == '123start'
        assert str(Safe_Str('123'       )) == '123'
        assert str(Safe_Str(123         )) == '123'
        assert str(Safe_Str('a'*256     )) == 'a'*256

        # Special characters get replaced with underscore
        assert str(Safe_Str('aaa_bbb')) == 'aaa_bbb'    # Underscore is replaced in base class
        assert str(Safe_Str('aaa-bbb')) == 'aaa_bbb'    # Hyphen is replaced
        assert str(Safe_Str('aaa.bbb')) == 'aaa_bbb'    # Period is replaced
        assert str(Safe_Str('aaa bbb')) == 'aaa_bbb'    # Space is replaced
        assert str(Safe_Str('aa   bb')) == 'aa___bb'    # Multiple spaces
        assert str(Safe_Str("aa ' bb")) == 'aa___bb'    # Quote is replaced

        # Trimming and other rules
        assert str(Safe_Str('  abc  '   )) == '__abc__'     # no default trimming
        assert str(Safe_Str('Abc-123!@#')) == 'Abc_123___'  # Mixed valid/invalid

        # Numeric values
        assert str(Safe_Str(12345  )) == '12345'
        assert str(Safe_Str(3.14159)) == '3_14159'      # Decimal point is replaced

        # Abuse cases
        assert str(Safe_Str('a!@£$b'    )) == 'a____b'
        assert str(Safe_Str('aaa/../'   )) == 'aaa____'
        assert str(Safe_Str('a\n\t\rb'  )) == 'a___b'
        assert str(Safe_Str('a\n\t\r'   )) == 'a___'
        assert str(Safe_Str('<script>alert("XSS")</script>')) == '_script_alert__XSS____script_'


        Safe_Str(''          )  # Empty string allowed
        Safe_Str(None        )  # None is allowed by default
        Safe_Str('!@#$%^&*()')  # All special chars allowed
        Safe_Str('______'    )  # All sanitised chars allowed
        Safe_Str('    '      )  # all strings allowed

        with pytest.raises(ValueError, match=f"in Safe_Str, value exceeds maximum length of {TYPE_SAFE__STR__MAX_LENGTH}") as exc_info:  # exceeds max length
            Safe_Str('a' * (TYPE_SAFE__STR__MAX_LENGTH + 1))

    def test_custom_subclass(self):
        # Create a subclass with custom settings for testing
        class Custom_Safe_Str(Safe_Str):
            max_length = 10
            allow_empty = True
            allow_all_replacement_char = True

        # Test custom settings
        assert str(Custom_Safe_Str('')) == ''  # Empty allowed
        assert str(Custom_Safe_Str(None)) == ''  # None becomes empty
        assert str(Custom_Safe_Str('!@#$%^')) == '______'  # All underscores allowed

        # Length validation still applies
        with pytest.raises(ValueError) as exc_info:
            Custom_Safe_Str('a' * 11)  # Exceeds custom max
        assert "in Custom_Safe_Str, value exceeds maximum length of 10" in str(exc_info.value)

    def test_custom_subclass__in_Type_safe(self):
        class Custom_Safe_Str(Safe_Str):
            max_length                 = 10
            allow_empty                = False
            allow_all_replacement_char = False
            trim_whitespace            = True

        class An_Class(Type_Safe):
            an_str : Custom_Safe_Str = Custom_Safe_Str('abc')

        an_class = An_Class()
        assert type(an_class.an_str      ) is Custom_Safe_Str
        assert base_types(an_class.an_str) == [Safe_Str, Type_Safe__Primitive, str, object, object]

        # expected_error = "Invalid type for attribute 'an_str'. Expected '<class 'test_Safe_Str.test_Safe_Str.test_custom_subclass__in_Type_safe.<locals>.Custom_Safe_Str'>' but got '<class 'str'>'"
        # with pytest.raises(ValueError, match=re.escape(expected_error)):
        #     an_class.an_str = 'xyz'

        #Edge cases: exceptions with specific error message checks
        with pytest.raises(ValueError, match="in Custom_Safe_Str, value cannot be None when allow_empty is False") as exc_info:
            Custom_Safe_Str(None)  # None is not allowed by default

        with pytest.raises(ValueError, match="in Custom_Safe_Str, value cannot be empty when allow_empty is False") as exc_info:
            Custom_Safe_Str('')  # Empty string is not allowed

        with pytest.raises(ValueError, match="in Custom_Safe_Str, sanitized value consists entirely of '_' characters") as exc_info:
          Custom_Safe_Str('!@#$%^&*()')

        with pytest.raises(ValueError, match="in Custom_Safe_Str, value cannot be empty when allow_empty is False") as exc_info:  # spaces only
            Custom_Safe_Str('    ')

        with pytest.raises(ValueError, match="in Custom_Safe_Str, sanitized value consists entirely of '_' characters") as exc_info:  # underscores only
            Custom_Safe_Str('______')

        an_class_round_trip = An_Class.from_json(an_class.json())
        assert an_class_round_trip.obj()        == an_class.obj()
        assert type(an_class_round_trip.an_str) is Custom_Safe_Str

    def test_usage_in_Type_Safe(self):
        class An_Class(Type_Safe):
            safe_str_1 : Safe_Str
            safe_str_2 : Safe_Str   = Safe_Str('abc'      )
            safe_str_3 : Safe_Str   = Safe_Str("aa**bb"   )
            safe_str_4 : Safe_Str   = Safe_Str("   abc   ")

        an_class = An_Class()
        assert type(an_class.safe_str_1) is Safe_Str
        assert type(an_class.safe_str_2) is Safe_Str
        assert type(an_class.safe_str_3) is Safe_Str
        assert type(an_class.safe_str_4) is Safe_Str

        assert an_class.obj() == __(safe_str_1 = ''             ,
                                    safe_str_2 = 'abc'          ,
                                    safe_str_3 = 'aa__bb'       ,
                                    safe_str_4 = '___abc___'    )

        from osbot_utils.utils.Dev import pprint
        assert an_class.json() == { 'safe_str_1': ''            ,
                                    'safe_str_2': 'abc'         ,
                                    'safe_str_3': 'aa__bb'      ,
                                    'safe_str_4': '___abc___'   }

        an_class__round_trip = An_Class.from_json(an_class.json())
        assert an_class__round_trip.obj() == an_class.obj()
        assert type(an_class__round_trip.safe_str_1) is Safe_Str
        assert type(an_class__round_trip.safe_str_2) is Safe_Str
        assert type(an_class__round_trip.safe_str_3) is Safe_Str
        assert type(an_class__round_trip.safe_str_4) is Safe_Str

    def test_strict_validation(self):
        # Create a subclass with strict validation for testing
        class Strict_Safe_Str(Safe_Str):
            regex = re.compile(r'[^a-zA-Z0-9]')  # Only alphanumeric allowed
            max_length = 20
            strict_validation = True  # Enable strict validation

        # Valid cases should pass
        assert str(Strict_Safe_Str('abc123')) == 'abc123'
        assert str(Strict_Safe_Str('ABC')) == 'ABC'
        assert str(Strict_Safe_Str('123')) == '123'

        # Invalid characters should raise exceptions
        with pytest.raises(ValueError, match="in Strict_Safe_Str, value contains invalid characters") as exc_info:
            Strict_Safe_Str('abc_123')  # Underscore is invalid

        with pytest.raises(ValueError, match="in Strict_Safe_Str, value contains invalid characters") as exc_info:
            Strict_Safe_Str('abc-123')  # Hyphen is invalid

        with pytest.raises(ValueError, match="in Strict_Safe_Str, value contains invalid characters") as exc_info:
            Strict_Safe_Str('abc 123')  # Space is invalid

        with pytest.raises(ValueError, match="in Strict_Safe_Str, value contains invalid characters") as exc_info:
            Strict_Safe_Str('abc.123')  # Period is invalid

        # Mixed valid/invalid
        with pytest.raises(ValueError, match="in Strict_Safe_Str, value contains invalid characters") as exc_info:
            Strict_Safe_Str('Abc-123!@#')

    def test_exact_length(self):
        # Create a subclass that requires exact length
        class ExactLength_Safe_Str(Safe_Str):
            max_length = 5
            exact_length = True  # Require exact length

        # Exact length should pass
        assert str(ExactLength_Safe_Str('abcde')) == 'abcde'
        assert str(ExactLength_Safe_Str('12345')) == '12345'

        # Too short should fail
        with pytest.raises(ValueError, match="in ExactLength_Safe_Str, value must be exactly 5 characters long") as exc_info:
            ExactLength_Safe_Str('abc')  # Too short

        # Too long should fail
        with pytest.raises(ValueError, match="in ExactLength_Safe_Str, value must be exactly 5 characters long") as exc_info:
            ExactLength_Safe_Str('abcdef')  # Too long

        # Empty string should fail
        #with pytest.raises(ValueError, match="in ExactLength_Safe_Str, value must be exactly 5 characters long") as exc_info:
        assert ExactLength_Safe_Str('') == '' # Empty

    def test_combined_strict_and_exact(self):
        # Create a subclass with both strict validation and exact length
        class Hash_Like_Str(Safe_Str):
            regex = re.compile(r'[^a-fA-F0-9]')  # Only hex characters
            max_length = 10
            strict_validation = True
            exact_length = True
            allow_empty = False
            trim_whitespace = True

        # Valid hash should pass
        assert str(Hash_Like_Str('0123456789')) == '0123456789'
        assert str(Hash_Like_Str('abcdef0123')) == 'abcdef0123'

        # Invalid length should fail
        with pytest.raises(ValueError, match="in Hash_Like_Str, value must be exactly 10 characters long") as exc_info:
            Hash_Like_Str('12345')  # Too short

        with pytest.raises(ValueError, match="in Hash_Like_Str, value must be exactly 10 characters long") as exc_info:
            Hash_Like_Str('12345678901')  # Too long

        # Invalid characters should fail
        with pytest.raises(ValueError, match="in Hash_Like_Str, value contains invalid characters") as exc_info:
            Hash_Like_Str('12345g7890')  # 'g' is not hex

        with pytest.raises(ValueError, match="in Hash_Like_Str, value contains invalid characters") as exc_info:
            Hash_Like_Str('1234-67890')  # '-' is not allowed

        # Spaces should be trimmed before validation
        with pytest.raises(ValueError, match="in Hash_Like_Str, value must be exactly 10 characters long") as exc_info:
            Hash_Like_Str(' 123456789 ')  # After trimming, it's only 9 chars

    def test__check__trim_whitespace__allow_all_replacement_char(self):
        class An_Safe_Str(Safe_Str):
            allow_empty                = True
            trim_whitespace            = True
            allow_all_replacement_char = False
        assert An_Safe_Str() == ''
        expected_message = "in An_Safe_Str, sanitized value consists entirely of '_' characters"
        with pytest.raises(ValueError, match=expected_message):
            An_Safe_Str('*')

    def test__regression__regex__allow_all_replacement_char(self):
        class An_Safe_Str(Safe_Str):
            regex                      = re.compile(r'^(?!https?://)')          # on this type of regex
            allow_all_replacement_char = False                                  # this will trigger the exception bellow

        #expected_message = "Sanitized value consists entirely of '_' characters"
        # with pytest.raises(ValueError, match=expected_message):
        #     An_Safe_Str("")                                                    #  BUG: should had not raised
        assert An_Safe_Str() == ''                                               # FIXED: correct behaviour
        assert An_Safe_Str(None) == ''
        assert An_Safe_Str('') == ''


    def test__json_serialisation(self):
        class An_Class(Type_Safe):
            an_safe_str: Safe_Str

        an_class = An_Class(an_safe_str='an_value')
        assert an_class.an_safe_str == 'an_value'
        assert an_class.obj ()      == __(an_safe_str=Safe_Str('an_value'))
        assert an_class.obj ()      == __(an_safe_str='an_value')
        assert an_class.json()      == {'an_safe_str': 'an_value'}

        from osbot_utils.utils.Dev import pprint
        assert type(an_class.json().get('an_safe_str')) is str                                   # BUG: this should be str

        roundtrip__an_class = An_Class.from_json(an_class.json())
        assert roundtrip__an_class.json() == {'an_safe_str': 'an_value'}
        assert roundtrip__an_class.json() == {'an_safe_str': Safe_Str('an_value')}
        assert roundtrip__an_class.obj () == __(an_safe_str=Safe_Str('an_value'))
        assert roundtrip__an_class.obj () == __(an_safe_str='an_value')

        assert json.dumps(an_class           .json()) == '{"an_safe_str": "an_value"}'
        assert json.dumps(roundtrip__an_class.json()) == '{"an_safe_str": "an_value"}'

    def test__str_concat_returns_safe_str_class(self):
        value_1 = Safe_Str('aaa')
        value_2 = Safe_Str('bbb')

        assert type(value_1) is Safe_Str
        assert type(value_2) is Safe_Str

        assert type(value_1 + 'xyz'  ) is Safe_Str           # confirms we keep the Safe_Str
        assert type(value_1 + value_2) is Safe_Str           # confirms we keep the Safe_Str

        with pytest.raises(TypeError, match=re.escape('can only concatenate str (not "int") to str')):
            type(value_1 + 123    )                     # OK: since we don't want to prevent non string concats

    def test__safe_str__string_representation(self):
        # Basic Safe_Str
        text = Safe_Str("Hello World")
        assert str(text) == "Hello_World"
        assert f"{text}" == "Hello_World"
        assert repr(text) == "Safe_Str('Hello_World')"

        # With sanitization
        text_sanitized = Safe_Str("Hello@World!")  # Should sanitize @ and !
        assert str(text_sanitized) == "Hello_World_"
        assert f"Message: {text_sanitized}" == "Message: Hello_World_"

    def test__safe_str__concatenation_preserves_representation(self):
        # After concatenation, string representation should still work
        str1 = Safe_Str("Hello")
        str2 = Safe_Str(" World")
        result = str1 + str2

        assert str(result) == "Hello_World"
        assert f"{result}!" == "Hello_World!"
        assert repr(result) == "Safe_Str('Hello_World')"

    def test__safe_str__string_methods_return_correct_types(self):
        # Ensure string methods that return strings maintain safe type
        text = Safe_Str("hello world")

        # These should return regular strings (not Safe_Str)
        assert type(text.upper()) is str
        assert text.upper() == "HELLO_WORLD"

        assert type(text.replace("world", "python")) is str
        assert text.replace("world", "python") == "hello_python"

        # But our concatenation returns Safe_Str
        assert type(text + "!") is Safe_Str

    def test_to_lower_case_feature(self):                                           # Test the new to_lower_case functionality
        # Create a subclass with lowercase enabled
        class Safe_Str__Lowercase(Safe_Str):
            to_lower_case = True

        # Basic lowercase conversion
        assert Safe_Str__Lowercase('HELLO')              == 'hello'
        assert Safe_Str__Lowercase('Hello World')        == 'hello_world'
        assert Safe_Str__Lowercase('MiXeD CaSe')         == 'mixed_case'
        assert Safe_Str__Lowercase('ABC123XYZ')          == 'abc123xyz'

        # Already lowercase stays lowercase
        assert Safe_Str__Lowercase('already lowercase')  == 'already_lowercase'
        assert Safe_Str__Lowercase('test123')            == 'test123'

        # Numbers and special chars (after sanitization)
        assert Safe_Str__Lowercase('Test-123')           == 'test_123'
        assert Safe_Str__Lowercase('USER@EMAIL')         == 'user_email'
        assert Safe_Str__Lowercase('File.Name.TXT')      == 'file_name_txt'

        # Empty and None handling
        assert Safe_Str__Lowercase('')                   == ''
        assert Safe_Str__Lowercase(None)                 == ''

    def test_to_lower_case_with_sanitization_order(self):                          # Test order of operations
        class Safe_Str__Email_Style(Safe_Str):
            to_lower_case = True
            regex         = re.compile(r'[^a-zA-Z0-9._]')

        # Sanitization happens before lowercase
        assert Safe_Str__Email_Style('John.DOE@test')    == 'john.doe_test'
        assert Safe_Str__Email_Style('User+Tag')         == 'user_tag'
        assert Safe_Str__Email_Style('ADMIN.USER')       == 'admin.user'

        # Complex cases
        assert Safe_Str__Email_Style('First.LAST+tag')   == 'first.last_tag'
        assert Safe_Str__Email_Style('USER_NAME.123')    == 'user_name.123'

    def test_to_lower_case_with_other_features(self):                             # Test interaction with other Safe_Str features
        class Safe_Str__Complex(Safe_Str):
            to_lower_case  = True
            trim_whitespace = True
            max_length     = 10

        # Trim + lowercase
        assert Safe_Str__Complex('  HELLO  ')            == 'hello'


        # Max length applied after lowercase
        error_message = "in Safe_Str__Complex, value exceeds maximum length of 10 characters (was 12)"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            assert Safe_Str__Complex('   SPACES HERE.   ')        # Also hits max_length
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__Complex('VERYLONGTEXT')

        # Combined transformations
        assert Safe_Str__Complex('       TEST 123       ')        == 'test_123'

    def test_to_lower_case_disabled_by_default(self):                             # Verify backward compatibility
        # Default Safe_Str should NOT lowercase
        assert Safe_Str('HELLO')                         == 'HELLO'
        assert Safe_Str('Mixed Case')                    == 'Mixed_Case'

        # Existing subclasses should not be affected
        class Safe_Str__NoLowercase(Safe_Str):
            max_length = 20
            # to_lower_case not set, should default to False

        assert Safe_Str__NoLowercase('UPPERCASE')       == 'UPPERCASE'
        assert Safe_Str__NoLowercase('MiXeD')           == 'MiXeD'

    def test_to_lower_case_with_strict_validation(self):                          # Test with strict validation mode
        class Safe_Str__Strict_Lower(Safe_Str):
            to_lower_case     = True
            strict_validation = True
            regex            = re.compile(r'[^a-z0-9]')  # Only lowercase allowed

        # Should lowercase first, then validate
        with pytest.raises(ValueError, match="value contains invalid characters"):
            Safe_Str__Strict_Lower('HELLO!')  # After lowercasing becomes 'hello!', but when strict checks the ! will trigger the exception


    def test_to_lower_case_unicode_handling(self):                                # Test unicode lowercase
        class Safe_Str__International(Safe_Str):
            to_lower_case = True
            regex        = re.compile(r'[^a-zA-ZÀ-ÿ0-9]')  # Allow accented chars

        # Unicode lowercase (if supported by regex)
        assert Safe_Str__International('CAFÉ')           == 'café'
        assert Safe_Str__International('MÜNCHEN')        == 'münchen'

        # Note: Actual behavior depends on regex pattern

    def test_to_lower_case_in_type_safe(self):                                   # Test usage in Type_Safe classes
        class Safe_Str__Username(Safe_Str):
            to_lower_case = True
            max_length   = 32
            regex        = re.compile(r'[^a-z0-9_]')

        class Schema__User(Type_Safe):
            username : Safe_Str__Username
            email    : Safe_Str__Username  # Reusing for email local part

        with Schema__User() as user:
            user.username = 'John_DOE'
            user.email    = 'ADMIn@TEST'

            assert user.username == 'john_doe'
            assert user.email    == 'admin_test'

            json_data = user.json()
            assert json_data['username'] == 'john_doe'
            assert json_data['email']    == 'admin_test'

    def test_to_lower_case_with_exact_length(self):                              # Test with exact_length requirement
        class Safe_Str__Fixed_Lower(Safe_Str):
            to_lower_case = True
            exact_length  = True
            max_length    = 5

        # Exact length after transformations
        assert Safe_Str__Fixed_Lower('HELLO')            == 'hello'
        assert Safe_Str__Fixed_Lower('AB123')            == 'ab123'

        # Wrong length should fail
        with pytest.raises(ValueError, match="must be exactly 5 characters long"):
            Safe_Str__Fixed_Lower('HI')  # Too short

        with pytest.raises(ValueError, match="must be exactly 5 characters long"):
            Safe_Str__Fixed_Lower('TOOLONG')  # Too long

    def test_to_lower_case_string_operations(self):                              # Test string operations preserve lowercase
        class Safe_Str__Lower(Safe_Str):
            to_lower_case = True

        text = Safe_Str__Lower('HELLO')
        assert text == 'hello'

        # Concatenation should preserve the class and apply lowercase
        result = text + 'WORLD'
        assert type(result) is Safe_Str__Lower
        assert result == 'helloworld'  # WORLD gets lowercased

        # F-string formatting
        assert f"{text}" == 'hello'

        # Repr shows the lowercased value
        assert repr(text) == "Safe_Str__Lower('hello')"