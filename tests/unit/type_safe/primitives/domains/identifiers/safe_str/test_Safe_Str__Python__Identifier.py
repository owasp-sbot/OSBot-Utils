import pytest
import keyword
from unittest                                                                                import TestCase

from osbot_utils.testing.__ import __
from osbot_utils.type_safe.Type_Safe                                                         import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Python__Identifier import Safe_Str__Python__Identifier
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Python__Module import Safe_Str__Python__Module


class test_Safe_Str__Python__Identifier(TestCase):

    def test__init__(self):                                      # Test basic initialization
        with Safe_Str__Python__Identifier() as _:
            assert type(_)                      is Safe_Str__Python__Identifier
            assert _.regex.pattern              == r'[^a-zA-Z0-9_]'              # Only letters, numbers, underscores
            assert _.replacement_char           == '_'
            assert _.to_lower_case              is False                         # Preserves case (unlike Safe_Str__Slug)
            assert _.allow_empty                is True                          # Can be empty
            assert _.trim_whitespace            is True
            assert _.max_length                 == 255

    def test_valid_identifiers(self):                            # Test valid Python identifier patterns
        # Basic identifiers
        assert str(Safe_Str__Python__Identifier('valid_name'         )) == 'valid_name'
        assert str(Safe_Str__Python__Identifier('another_valid'      )) == 'another_valid'
        assert str(Safe_Str__Python__Identifier('my_var'             )) == 'my_var'
        assert str(Safe_Str__Python__Identifier('some_function'      )) == 'some_function'

        # With numbers
        assert str(Safe_Str__Python__Identifier('var_1'              )) == 'var_1'
        assert str(Safe_Str__Python__Identifier('item_123'           )) == 'item_123'
        assert str(Safe_Str__Python__Identifier('data2024'           )) == 'data2024'

        # Starting with underscore
        assert str(Safe_Str__Python__Identifier('_private'           )) == '_private'
        assert str(Safe_Str__Python__Identifier('__dunder__'         )) == '__dunder__'
        assert str(Safe_Str__Python__Identifier('_'                  )) == '_'

        # CamelCase and mixed case (case is preserved)
        assert str(Safe_Str__Python__Identifier('CamelCase'          )) == 'CamelCase'
        assert str(Safe_Str__Python__Identifier('mixedCase123'       )) == 'mixedCase123'
        assert str(Safe_Str__Python__Identifier('PascalCase'         )) == 'PascalCase'

        # All caps
        assert str(Safe_Str__Python__Identifier('CONSTANT'           )) == 'CONSTANT'
        assert str(Safe_Str__Python__Identifier('MAX_VALUE'          )) == 'MAX_VALUE'

    def test_invalid_starting_character(self):                   # Test handling of invalid starting characters
        # Numbers at start get prefixed with underscore
        assert str(Safe_Str__Python__Identifier('123'                )) == '_123'
        assert str(Safe_Str__Python__Identifier('8b1a9953c4'         )) == '_8b1a9953c4'                # Hash value case
        assert str(Safe_Str__Python__Identifier('42answer'           )) == '_42answer'
        assert str(Safe_Str__Python__Identifier('0index'             )) == '_0index'

        # Special characters at start get replaced then prefixed
        assert str(Safe_Str__Python__Identifier('$var'               )) == '_var'                       # $ replaced first, which will make it already _ prefixed (so no need to prefix it again)
        assert str(Safe_Str__Python__Identifier('@property'          )) == '_property'                  # ... same thing for all of these
        assert str(Safe_Str__Python__Identifier('#tag'               )) == '_tag'
        assert str(Safe_Str__Python__Identifier('-negative'          )) == '_negative'

    def test_special_character_replacement(self):                # Test replacement of invalid characters
        # Spaces replaced with underscores
        assert str(Safe_Str__Python__Identifier('hello world'        )) == 'hello_world'
        assert str(Safe_Str__Python__Identifier('my var name'        )) == 'my_var_name'

        # Hyphens replaced (unlike slugs which preserve them)
        assert str(Safe_Str__Python__Identifier('my-var-name'        )) == 'my_var_name'
        assert str(Safe_Str__Python__Identifier('snake-case'         )) == 'snake_case'
        assert str(Safe_Str__Python__Identifier('kebab-case-style'   )) == 'kebab_case_style'

        # Special characters replaced
        assert str(Safe_Str__Python__Identifier('hello@world'        )) == 'hello_world'
        assert str(Safe_Str__Python__Identifier('price:$100'         )) == 'price__100'
        assert str(Safe_Str__Python__Identifier('100%'               )) == '_100_'                      # Number start + % replaced
        assert str(Safe_Str__Python__Identifier('Q&A'                )) == 'Q_A'
        assert str(Safe_Str__Python__Identifier("it's"               )) == 'it_s'

        # Dots replaced
        assert str(Safe_Str__Python__Identifier('file.name'          )) == 'file_name'
        assert str(Safe_Str__Python__Identifier('version.1.0'        )) == 'version_1_0'

        # Slashes replaced
        assert str(Safe_Str__Python__Identifier('path/to/file'       )) == 'path_to_file'
        assert str(Safe_Str__Python__Identifier('namespace::func'    )) == 'namespace__func'

        # Multiple consecutive special chars
        assert str(Safe_Str__Python__Identifier('hello!!!world'      )) == 'hello___world'
        assert str(Safe_Str__Python__Identifier('var---name'         )) == 'var___name'

    def test_python_keyword_handling(self):                      # Test Python keyword collision prevention
        # Python keywords get prefixed with underscore
        assert str(Safe_Str__Python__Identifier('class'              )) == '_class'
        assert str(Safe_Str__Python__Identifier('def'                )) == '_def'
        assert str(Safe_Str__Python__Identifier('return'             )) == '_return'
        assert str(Safe_Str__Python__Identifier('if'                 )) == '_if'
        assert str(Safe_Str__Python__Identifier('else'               )) == '_else'
        assert str(Safe_Str__Python__Identifier('for'                )) == '_for'
        assert str(Safe_Str__Python__Identifier('while'              )) == '_while'
        assert str(Safe_Str__Python__Identifier('import'             )) == '_import'
        assert str(Safe_Str__Python__Identifier('from'               )) == '_from'
        assert str(Safe_Str__Python__Identifier('try'                )) == '_try'
        assert str(Safe_Str__Python__Identifier('except'             )) == '_except'
        assert str(Safe_Str__Python__Identifier('finally'            )) == '_finally'
        assert str(Safe_Str__Python__Identifier('lambda'             )) == '_lambda'
        assert str(Safe_Str__Python__Identifier('with'               )) == '_with'
        assert str(Safe_Str__Python__Identifier('as'                 )) == '_as'
        assert str(Safe_Str__Python__Identifier('pass'               )) == '_pass'
        assert str(Safe_Str__Python__Identifier('break'              )) == '_break'
        assert str(Safe_Str__Python__Identifier('continue'           )) == '_continue'
        assert str(Safe_Str__Python__Identifier('yield'              )) == '_yield'
        assert str(Safe_Str__Python__Identifier('global'             )) == '_global'
        assert str(Safe_Str__Python__Identifier('nonlocal'           )) == '_nonlocal'

        # these also are converted
        assert str(Safe_Str__Python__Identifier('True'               )) == '_True'
        assert str(Safe_Str__Python__Identifier('False'              )) == '_False'

        # Builtin names that aren't keywords are allowed (they shadow builtins but are valid identifiers)
        assert str(Safe_Str__Python__Identifier('list'               )) == 'list'                       # Not a keyword
        assert str(Safe_Str__Python__Identifier('dict'               )) == 'dict'
        assert str(Safe_Str__Python__Identifier('str'                )) == 'str'
        assert str(Safe_Str__Python__Identifier('int'                )) == 'int'
        assert str(Safe_Str__Python__Identifier('print'              )) == 'print'

    def test_case_preservation(self):                            # Test that case is preserved (unlike Safe_Str__Slug)
        # Mixed case preserved
        assert str(Safe_Str__Python__Identifier('MyVariable'         )) == 'MyVariable'
        assert str(Safe_Str__Python__Identifier('camelCase'          )) == 'camelCase'
        assert str(Safe_Str__Python__Identifier('PascalCase'         )) == 'PascalCase'
        assert str(Safe_Str__Python__Identifier('snake_Case'         )) == 'snake_Case'

        # Uppercase preserved
        assert str(Safe_Str__Python__Identifier('CONSTANT_VALUE'     )) == 'CONSTANT_VALUE'
        assert str(Safe_Str__Python__Identifier('API_KEY'            )) == 'API_KEY'

    def test_whitespace_trimming(self):                          # Test whitespace handling
        assert str(Safe_Str__Python__Identifier('  var  '            )) == 'var'
        assert str(Safe_Str__Python__Identifier('\tvalue\t'          )) == 'value'
        assert str(Safe_Str__Python__Identifier('\ndata\n'           )) == 'data'
        assert str(Safe_Str__Python__Identifier('  my_var  '         )) == 'my_var'

    def test_empty_string_handling(self):                        # Test empty string becomes underscore
        # Empty strings become single underscore
        assert str(Safe_Str__Python__Identifier(''                   )) == '_'
        assert str(Safe_Str__Python__Identifier(None                 )) == '_'
        assert str(Safe_Str__Python__Identifier('   '                )) == '_'                          # Whitespace-only

        # Special chars only also become underscore
        assert str(Safe_Str__Python__Identifier('!!!'                )) == '___'                        # Each ! becomes _, but then starts with digit? No, starts with _
        assert str(Safe_Str__Python__Identifier('$$$'                )) == '___'

    def test_type_conversion(self):                              # Test conversion from other types
        # From integer
        assert str(Safe_Str__Python__Identifier(123                  )) == '_123'                       # Number start
        assert str(Safe_Str__Python__Identifier(0                    )) == '_0'

        # From float
        assert str(Safe_Str__Python__Identifier(123.456              )) == '_123_456'                   # Dot replaced, number start
        assert str(Safe_Str__Python__Identifier(1.0                  )) == '_1_0'

        # From boolean
        assert str(Safe_Str__Python__Identifier(True                 )) == '_True'                       # Valid identifier
        assert str(Safe_Str__Python__Identifier(False                )) == '_False'

    def test_hash_value_use_case(self):                          # Test the original use case - hash values as identifiers
        # Hash values starting with numbers
        assert str(Safe_Str__Python__Identifier('8b1a9953c4'         )) == '_8b1a9953c4'
        assert str(Safe_Str__Python__Identifier('a1b2c3d4e5'         )) == 'a1b2c3d4e5'                # Starts with letter
        assert str(Safe_Str__Python__Identifier('1234567890'         )) == '_1234567890'
        assert str(Safe_Str__Python__Identifier('abc123def456'       )) == 'abc123def456'

        # UUIDs with hyphens
        assert str(Safe_Str__Python__Identifier('550e8400-e29b-41d4' )) == '_550e8400_e29b_41d4'        # Number start + hyphens replaced

    def test_dict_key_scenarios(self):                           # Test common dict key transformation scenarios
        # Keys that need transformation
        assert str(Safe_Str__Python__Identifier('user-id'            )) == 'user_id'
        assert str(Safe_Str__Python__Identifier('first-name'         )) == 'first_name'
        assert str(Safe_Str__Python__Identifier('api-key'            )) == 'api_key'
        assert str(Safe_Str__Python__Identifier('max-length'         )) == 'max_length'

        # Numeric keys
        assert str(Safe_Str__Python__Identifier('0'                  )) == '_0'
        assert str(Safe_Str__Python__Identifier('42'                 )) == '_42'

    def test_in_type_safe_schema(self):                          # Test usage in Type_Safe classes
        class Schema__Test(Type_Safe):
            identifier1 : Safe_Str__Python__Identifier
            identifier2 : Safe_Str__Python__Identifier
            identifier3 : Safe_Str__Python__Identifier

        with Schema__Test() as _:
            # Auto-initialization
            assert type(_.identifier1) is Safe_Str__Python__Identifier
            assert type(_.identifier2) is Safe_Str__Python__Identifier
            assert type(_.identifier3) is Safe_Str__Python__Identifier

            # Setting with raw strings (auto-conversion)
            _.identifier1 = '8b1a9953c4'                                                               # Hash value
            assert _.identifier1 == '_8b1a9953c4'

            # Setting with special characters
            _.identifier2 = 'my-variable-name'
            assert _.identifier2 == 'my_variable_name'

            # Setting with keyword
            _.identifier3 = 'class'
            assert _.identifier3 == '_class'

            # JSON serialization
            json_data = _.json()
            assert json_data['identifier1'] == '_8b1a9953c4'
            assert json_data['identifier2'] == 'my_variable_name'
            assert json_data['identifier3'] == '_class'

            assert _.obj() == __(identifier1 = '_8b1a9953c4'     ,
                                 identifier2 = 'my_variable_name',
                                 identifier3 = '_class'          )

    def test_max_length_constraint(self):                        # Test length limits
        max_length = 255
        max_identifier = 'a' * max_length
        assert str(Safe_Str__Python__Identifier(max_identifier)) == max_identifier
        assert len(Safe_Str__Python__Identifier(max_identifier)) == max_length

        # Exceeds max length
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Python__Identifier('a' * (max_length + 1))
        assert f"value exceeds maximum length of {max_length}" in str(exc_info.value)

    def test_unicode_handling(self):                             # Test Unicode character handling
        # Unicode letters get replaced
        assert str(Safe_Str__Python__Identifier('café'               )) == 'caf_'
        assert str(Safe_Str__Python__Identifier('naïve'              )) == 'na_ve'
        assert str(Safe_Str__Python__Identifier('Zürich'             )) == 'Z_rich'
        assert str(Safe_Str__Python__Identifier('世界'               )) == '__'                                # Non-Latin chars replaced

    def test_real_world_transformations(self):                   # Test realistic transformation scenarios
        # API response keys
        assert str(Safe_Str__Python__Identifier('user-id'            )) == 'user_id'
        assert str(Safe_Str__Python__Identifier('created-at'         )) == 'created_at'
        assert str(Safe_Str__Python__Identifier('Content-Type'       )) == 'Content_Type'

        # Database column names
        assert str(Safe_Str__Python__Identifier('user.name'          )) == 'user_name'
        assert str(Safe_Str__Python__Identifier('order.total'        )) == 'order_total'

        # File paths as identifiers
        assert str(Safe_Str__Python__Identifier('src/main.py'        )) == 'src_main_py'
        assert str(Safe_Str__Python__Identifier('test/test_main.py'  )) == 'test_test_main_py'

    def test_comparison_with_string(self):                       # Test equality comparisons
        identifier = Safe_Str__Python__Identifier('test_var')
        assert identifier == 'test_var'
        assert identifier != 'other_var'
        assert str(identifier) == 'test_var'

    def test_edge_cases(self):                                   # Test edge cases
        # Single underscore is valid
        assert str(Safe_Str__Python__Identifier('_'                  )) == '_'

        # Multiple underscores
        assert str(Safe_Str__Python__Identifier('___'                )) == '___'

        # Mix of valid and invalid
        assert str(Safe_Str__Python__Identifier('valid_name!'        )) == 'valid_name_'
        assert str(Safe_Str__Python__Identifier('_private$'          )) == '_private_'

    def test_difference_from_python_module(self):                # Compare with Safe_Str__Python__Module
        test_string = 'My-Module-Name'

        # Safe_Str__Python__Identifier preserves case
        identifier = Safe_Str__Python__Identifier(test_string)
        assert str(identifier) == 'My_Module_Name'                                                    # Case preserved, hyphen replaced

        # Safe_Str__Python__Module forces lowercase
        module = Safe_Str__Python__Module(test_string)
        assert str(module) == 'my_module_name'                                                        # Lowercase, hyphen replaced

        # This distinction is important for:
        # - Variable names (case-sensitive)
        # - Module names (lowercase convention)

    def test_keyword_module_reference(self):                     # Verify all Python keywords are handled
        # Test ALL Python keywords to ensure comprehensive coverage
        all_keywords = keyword.kwlist
        for kw in all_keywords:
            result = str(Safe_Str__Python__Identifier(kw))
            assert result == f'_{kw}', f"Keyword '{kw}' should become '_{kw}' but got '{result}'"
            assert result.isidentifier(), f"Result '{result}' is not a valid identifier"
            assert not keyword.iskeyword(result), f"Result '{result}' is still a keyword"