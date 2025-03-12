import re
import pytest
from unittest                              import TestCase
from osbot_utils.helpers.safe_str.Safe_Str import Safe_Str, TYPE_SAFE__STR__MAX_LENGTH
from osbot_utils.type_safe.Type_Safe       import Type_Safe
from osbot_utils.utils.Objects             import __, base_types


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

        with pytest.raises(ValueError, match=f"Value exceeds maximum length of {TYPE_SAFE__STR__MAX_LENGTH}") as exc_info:  # exceeds max length
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
        assert "Value exceeds maximum length of 10" in str(exc_info.value)

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
        assert base_types(an_class.an_str) == [Safe_Str, str, object]

        expected_error = "Invalid type for attribute 'an_str'. Expected '<class 'test_Safe_Str.test_Safe_Str.test_custom_subclass__in_Type_safe.<locals>.Custom_Safe_Str'>' but got '<class 'str'>'"
        with pytest.raises(ValueError, match=re.escape(expected_error)):
            an_class.an_str = 'xyz'

        #Edge cases: exceptions with specific error message checks
        with pytest.raises(ValueError, match="Value cannot be None when allow_empty is False") as exc_info:
            Custom_Safe_Str(None)  # None is not allowed by default

        with pytest.raises(ValueError, match="Value cannot be empty when allow_empty is False") as exc_info:
            Custom_Safe_Str('')  # Empty string is not allowed

        with pytest.raises(ValueError, match="Sanitized value consists entirely of '_' characters") as exc_info:
          Custom_Safe_Str('!@#$%^&*()')

        with pytest.raises(ValueError, match="Value cannot be empty when allow_empty is False") as exc_info:  # spaces only
            Custom_Safe_Str('    ')

        with pytest.raises(ValueError, match="Sanitized value consists entirely of '_' characters") as exc_info:  # underscores only
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
        with pytest.raises(ValueError, match="Value contains invalid characters") as exc_info:
            Strict_Safe_Str('abc_123')  # Underscore is invalid

        with pytest.raises(ValueError, match="Value contains invalid characters") as exc_info:
            Strict_Safe_Str('abc-123')  # Hyphen is invalid

        with pytest.raises(ValueError, match="Value contains invalid characters") as exc_info:
            Strict_Safe_Str('abc 123')  # Space is invalid

        with pytest.raises(ValueError, match="Value contains invalid characters") as exc_info:
            Strict_Safe_Str('abc.123')  # Period is invalid

        # Mixed valid/invalid
        with pytest.raises(ValueError, match="Value contains invalid characters") as exc_info:
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
        with pytest.raises(ValueError, match="Value must be exactly 5 characters long") as exc_info:
            ExactLength_Safe_Str('abc')  # Too short

        # Too long should fail
        with pytest.raises(ValueError, match="Value must be exactly 5 characters long") as exc_info:
            ExactLength_Safe_Str('abcdef')  # Too long

        # Empty string should fail
        with pytest.raises(ValueError, match="Value must be exactly 5 characters long") as exc_info:
            ExactLength_Safe_Str('')  # Empty

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
        with pytest.raises(ValueError, match="Value must be exactly 10 characters long") as exc_info:
            Hash_Like_Str('12345')  # Too short

        with pytest.raises(ValueError, match="Value must be exactly 10 characters long") as exc_info:
            Hash_Like_Str('12345678901')  # Too long

        # Invalid characters should fail
        with pytest.raises(ValueError, match="Value contains invalid characters") as exc_info:
            Hash_Like_Str('12345g7890')  # 'g' is not hex

        with pytest.raises(ValueError, match="Value contains invalid characters") as exc_info:
            Hash_Like_Str('1234-67890')  # '-' is not allowed

        # Spaces should be trimmed before validation
        with pytest.raises(ValueError, match="Value must be exactly 10 characters long") as exc_info:
            Hash_Like_Str(' 123456789 ')  # After trimming, it's only 9 chars