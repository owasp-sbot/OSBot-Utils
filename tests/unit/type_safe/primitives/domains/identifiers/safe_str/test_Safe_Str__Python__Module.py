import pytest
from unittest                                                                                import TestCase
from osbot_utils.type_safe.Type_Safe                                                         import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Python__Identifier import Safe_Str__Python__Identifier
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Python__Module import Safe_Str__Python__Module


class test_Safe_Str__Python__Module(TestCase):

    def test__init__(self):                                      # Test basic initialization
        with Safe_Str__Python__Module() as _:
            assert type(_)                      is Safe_Str__Python__Module
            assert _.regex.pattern              == r'[^a-z0-9_]'                # Only lowercase, numbers, underscores
            assert _.replacement_char           == '_'
            assert _.to_lower_case              is True                         # CRITICAL: Forces lowercase
            assert _.allow_empty                is True
            assert _.trim_whitespace            is True
            assert _.max_length                 == 64

    def test_valid_module_names(self):                           # Test valid Python module patterns
        # Basic module names
        assert str(Safe_Str__Python__Module('users'              )) == 'users'
        assert str(Safe_Str__Python__Module('admin'              )) == 'admin'
        assert str(Safe_Str__Python__Module('api'                )) == 'api'
        assert str(Safe_Str__Python__Module('models'             )) == 'models'

        # With underscores
        assert str(Safe_Str__Python__Module('file_store'         )) == 'file_store'
        assert str(Safe_Str__Python__Module('api_v1'             )) == 'api_v1'
        assert str(Safe_Str__Python__Module('user_service'       )) == 'user_service'
        assert str(Safe_Str__Python__Module('data_models'        )) == 'data_models'

        # With numbers
        assert str(Safe_Str__Python__Module('module_v1'          )) == 'module_v1'
        assert str(Safe_Str__Python__Module('api_v2'             )) == 'api_v2'
        assert str(Safe_Str__Python__Module('test_123'           )) == 'test_123'

        # Starting with underscore (private modules)
        assert str(Safe_Str__Python__Module('_private'           )) == '_private'
        assert str(Safe_Str__Python__Module('_internal'          )) == '_internal'
        assert str(Safe_Str__Python__Module('__main__'           )) == '__main__'

        # Common Python module patterns
        assert str(Safe_Str__Python__Module('utils'              )) == 'utils'
        assert str(Safe_Str__Python__Module('helpers'            )) == 'helpers'
        assert str(Safe_Str__Python__Module('config'             )) == 'config'
        assert str(Safe_Str__Python__Module('settings'           )) == 'settings'

    def test_lowercase_conversion(self):                         # Test automatic lowercase conversion
        # Uppercase converted to lowercase
        assert str(Safe_Str__Python__Module('USERS'              )) == 'users'
        assert str(Safe_Str__Python__Module('API'                )) == 'api'
        assert str(Safe_Str__Python__Module('Models'             )) == 'models'
        assert str(Safe_Str__Python__Module('CONFIG'             )) == 'config'

        # Mixed case converted
        assert str(Safe_Str__Python__Module('UserService'        )) == 'userservice'
        assert str(Safe_Str__Python__Module('ApiClient'          )) == 'apiclient'
        assert str(Safe_Str__Python__Module('DataModels'         )) == 'datamodels'

        # CamelCase becomes lowercase (no separation)
        assert str(Safe_Str__Python__Module('CamelCase'          )) == 'camelcase'
        assert str(Safe_Str__Python__Module('PascalCase'         )) == 'pascalcase'
        assert str(Safe_Str__Python__Module('mixedCase'          )) == 'mixedcase'

    def test_invalid_starting_character(self):                   # Test handling of invalid starting characters
        # Numbers at start get prefixed with underscore
        assert str(Safe_Str__Python__Module('123'                )) == '_123'
        assert str(Safe_Str__Python__Module('8module'            )) == '_8module'
        assert str(Safe_Str__Python__Module('42answer'           )) == '_42answer'
        assert str(Safe_Str__Python__Module('0index'             )) == '_0index'

        # Special characters at start get replaced then prefixed
        assert str(Safe_Str__Python__Module('$var'               )) == '_var'                            # $ replaced, no need to do anything else
        assert str(Safe_Str__Python__Module('@property'          )) == '_property'
        assert str(Safe_Str__Python__Module('#tag'               )) == '_tag'
        assert str(Safe_Str__Python__Module('-module'            )) == '_module'

    def test_character_sanitization(self):                       # Test character replacement
        # Hyphens replaced with underscores
        assert str(Safe_Str__Python__Module('api-v1'             )) == 'api_v1'
        assert str(Safe_Str__Python__Module('user-service'       )) == 'user_service'
        assert str(Safe_Str__Python__Module('file-store'         )) == 'file_store'
        assert str(Safe_Str__Python__Module('my-module-name'     )) == 'my_module_name'

        # Dots replaced (important for package names)
        assert str(Safe_Str__Python__Module('api.v1'             )) == 'api_v1'
        assert str(Safe_Str__Python__Module('users.models'       )) == 'users_models'
        assert str(Safe_Str__Python__Module('file.utils'         )) == 'file_utils'

        # Slashes replaced (converting paths)
        assert str(Safe_Str__Python__Module('api/v1'             )) == 'api_v1'
        assert str(Safe_Str__Python__Module('src/models'         )) == 'src_models'
        assert str(Safe_Str__Python__Module('utils/helpers'      )) == 'utils_helpers'

        # Spaces replaced
        assert str(Safe_Str__Python__Module('user service'       )) == 'user_service'
        assert str(Safe_Str__Python__Module('api client'         )) == 'api_client'

        # Special characters replaced
        assert str(Safe_Str__Python__Module('api@v1'             )) == 'api_v1'
        assert str(Safe_Str__Python__Module('user:service'       )) == 'user_service'
        assert str(Safe_Str__Python__Module('file$store'         )) == 'file_store'
        assert str(Safe_Str__Python__Module('{users}'            )) == '_users_'

        # Brackets and braces
        assert str(Safe_Str__Python__Module('[module]'           )) == '_module_'
        assert str(Safe_Str__Python__Module('(helper)'           )) == '_helper_'

        # Multiple consecutive special chars
        assert str(Safe_Str__Python__Module('api---v1'           )) == 'api___v1'
        assert str(Safe_Str__Python__Module('user:::service'     )) == 'user___service'

    def test_whitespace_trimming(self):                          # Test whitespace handling
        assert str(Safe_Str__Python__Module('  module  '         )) == 'module'
        assert str(Safe_Str__Python__Module('\tutils\t'          )) == 'utils'
        assert str(Safe_Str__Python__Module('\nconfig\n'         )) == 'config'
        assert str(Safe_Str__Python__Module('  my_module  '      )) == 'my_module'

    def test_empty_string_handling(self):                        # Test empty string behavior
        # Empty strings allowed (returns empty string)
        assert str(Safe_Str__Python__Module(''                   )) == ''
        assert str(Safe_Str__Python__Module(None                 )) == ''
        assert str(Safe_Str__Python__Module('   '                )) == ''                              # Whitespace-only

    def test_type_conversion(self):                              # Test conversion from other types
        # From integer
        assert str(Safe_Str__Python__Module(123                  )) == '_123'                          # Number start
        assert str(Safe_Str__Python__Module(0                    )) == '_0'

        # From float
        assert str(Safe_Str__Python__Module(123.456              )) == '_123_456'                      # Dot replaced, number start
        assert str(Safe_Str__Python__Module(1.0                  )) == '_1_0'

        # From boolean (lowercased)
        assert str(Safe_Str__Python__Module(True                 )) == 'true'                          # Lowercase
        assert str(Safe_Str__Python__Module(False                )) == 'false'

    def test_common_module_patterns(self):                       # Test real-world module naming patterns
        # Standard library style
        assert str(Safe_Str__Python__Module('os'                 )) == 'os'
        assert str(Safe_Str__Python__Module('sys'                )) == 'sys'
        assert str(Safe_Str__Python__Module('json'               )) == 'json'
        assert str(Safe_Str__Python__Module('datetime'           )) == 'datetime'

        # Package style (but single component)
        assert str(Safe_Str__Python__Module('osbot_utils'        )) == 'osbot_utils'
        assert str(Safe_Str__Python__Module('type_safe'          )) == 'type_safe'
        assert str(Safe_Str__Python__Module('user_service'       )) == 'user_service'

        # Version suffixes
        assert str(Safe_Str__Python__Module('api_v1'             )) == 'api_v1'
        assert str(Safe_Str__Python__Module('api_v2'             )) == 'api_v2'
        assert str(Safe_Str__Python__Module('module_2024'        )) == 'module_2024'

        # Test/dev modules
        assert str(Safe_Str__Python__Module('test_utils'         )) == 'test_utils'
        assert str(Safe_Str__Python__Module('test_models'        )) == 'test_models'
        assert str(Safe_Str__Python__Module('dev_tools'          )) == 'dev_tools'

    def test_package_name_conversion(self):                      # Test converting package-style names
        # Dotted package names become single module names
        assert str(Safe_Str__Python__Module('osbot.utils'        )) == 'osbot_utils'
        assert str(Safe_Str__Python__Module('django.core'        )) == 'django_core'
        assert str(Safe_Str__Python__Module('flask.app'          )) == 'flask_app'

        # Multi-level packages
        assert str(Safe_Str__Python__Module('a.b.c'              )) == 'a_b_c'
        assert str(Safe_Str__Python__Module('api.v1.users'       )) == 'api_v1_users'

    def test_path_to_module_conversion(self):                    # Test converting file paths to module names
        # Unix-style paths
        assert str(Safe_Str__Python__Module('src/utils'          )) == 'src_utils'
        assert str(Safe_Str__Python__Module('api/v1/users'       )) == 'api_v1_users'
        assert str(Safe_Str__Python__Module('tests/unit/models'  )) == 'tests_unit_models'

        # Windows-style paths
        assert str(Safe_Str__Python__Module('src\\utils'         )) == 'src_utils'
        assert str(Safe_Str__Python__Module('api\\v1\\users'     )) == 'api_v1_users'

        # With file extension
        assert str(Safe_Str__Python__Module('module.py'          )) == 'module_py'
        assert str(Safe_Str__Python__Module('utils.py'           )) == 'utils_py'

    def test_kebab_case_to_snake_case(self):                     # Test converting kebab-case to snake_case
        # Kebab-case (common in URLs/repos) becomes snake_case
        assert str(Safe_Str__Python__Module('user-service'       )) == 'user_service'
        assert str(Safe_Str__Python__Module('api-client'         )) == 'api_client'
        assert str(Safe_Str__Python__Module('data-models'        )) == 'data_models'
        assert str(Safe_Str__Python__Module('file-store-v2'      )) == 'file_store_v2'

    def test_in_type_safe_schema(self):                          # Test usage in Type_Safe classes
        class Schema__Package(Type_Safe):
            module_name  : Safe_Str__Python__Module
            package_name : Safe_Str__Python__Module
            submodule    : Safe_Str__Python__Module

        with Schema__Package() as _:
            # Auto-initialization
            assert type(_.module_name ) is Safe_Str__Python__Module
            assert type(_.package_name) is Safe_Str__Python__Module
            assert type(_.submodule   ) is Safe_Str__Python__Module

            # Setting with raw strings (auto-conversion)
            _.module_name = 'UserService'                                                              # CamelCase
            assert _.module_name == 'userservice'                                                     # Lowercase, no separation

            # Setting with special characters
            _.package_name = 'api-client-v2'                                                          # Kebab-case
            assert _.package_name == 'api_client_v2'

            # Setting with path
            _.submodule = 'src/models/user'
            assert _.submodule == 'src_models_user'

            # JSON serialization
            json_data = _.json()
            assert json_data['module_name' ] == 'userservice'
            assert json_data['package_name'] == 'api_client_v2'
            assert json_data['submodule'   ] == 'src_models_user'

    def test_max_length_constraint(self):                        # Test length limits
        max_length = 64
        max_module = 'a' * max_length
        assert str(Safe_Str__Python__Module(max_module)) == max_module
        assert len(Safe_Str__Python__Module(max_module)) == max_length

        # Exceeds max length
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Python__Module('a' * (max_length + 1))
        assert f"value exceeds maximum length of {max_length}" in str(exc_info.value)

    def test_unicode_handling(self):                             # Test Unicode character handling
        # Unicode letters get replaced and lowercased
        assert str(Safe_Str__Python__Module('café'               )) == 'caf_'
        assert str(Safe_Str__Python__Module('naïve'              )) == 'na_ve'
        assert str(Safe_Str__Python__Module('Zürich'             )) == 'z_rich'                        # Lowercased
        assert str(Safe_Str__Python__Module('世界'               )) == '__'                             # Non-Latin chars replaced

    def test_file_system_safety(self):                           # Test that names are safe on all platforms
        # No problematic characters for filesystems
        problematic = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
        for char in problematic:
            result = str(Safe_Str__Python__Module(f'test{char}module'))
            assert char not in result
            assert '_' in result                                                                      # Replaced with underscore

        # Windows reserved names should still be allowed (they're valid Python)
        assert str(Safe_Str__Python__Module('con'                )) == 'con'                          # Valid module name
        assert str(Safe_Str__Python__Module('aux'                )) == 'aux'
        assert str(Safe_Str__Python__Module('nul'                )) == 'nul'

    def test_comparison_with_string(self):                       # Test equality comparisons
        module = Safe_Str__Python__Module('test_module')
        assert module == 'test_module'
        assert module != 'other_module'
        assert str(module) == 'test_module'

    def test_edge_cases(self):                                   # Test edge cases
        # Single character
        assert str(Safe_Str__Python__Module('a'                  )) == 'a'
        assert str(Safe_Str__Python__Module('z'                  )) == 'z'
        assert str(Safe_Str__Python__Module('_'                  )) == '_'

        # Numbers only
        assert str(Safe_Str__Python__Module('123'                )) == '_123'                         # Must prefix

        # All underscores
        assert str(Safe_Str__Python__Module('___'                )) == '___'

        # Mix of valid and invalid
        assert str(Safe_Str__Python__Module('valid_name!'        )) == 'valid_name_'
        assert str(Safe_Str__Python__Module('_private$'          )) == '_private_'

    def test_difference_from_identifier(self):                   # Compare with Safe_Str__Python__Identifier
        test_string = 'My-Module-Name'

        # Safe_Str__Python__Module forces lowercase
        module = Safe_Str__Python__Module(test_string)
        assert str(module) == 'my_module_name'                                                        # Lowercase

        # Safe_Str__Python__Identifier preserves case
        identifier = Safe_Str__Python__Identifier(test_string)
        assert str(identifier) == 'My_Module_Name'                                                    # Case preserved

        # This distinction is important for:
        # - Module names (PEP 8 recommends lowercase)
        # - Variable names (case-sensitive)

    def test_pep8_module_naming_convention(self):                # Test PEP 8 compliance
        # PEP 8 recommends lowercase with underscores for modules
        assert str(Safe_Str__Python__Module('MyModule'           )) == 'mymodule'                     # Not My_Module
        assert str(Safe_Str__Python__Module('UserService'        )) == 'userservice'                  # Not User_Service

        # This is correct because:
        # - PEP 8: "Modules should have short, all-lowercase names"
        # - Underscores can be used if it improves readability, but not required

    def test_private_module_convention(self):                    # Test private/internal module patterns
        # Single underscore prefix (internal use)
        assert str(Safe_Str__Python__Module('_internal'          )) == '_internal'
        assert str(Safe_Str__Python__Module('_utils'             )) == '_utils'
        assert str(Safe_Str__Python__Module('_helpers'           )) == '_helpers'

        # Double underscore (name mangling)
        assert str(Safe_Str__Python__Module('__private'          )) == '__private'
        assert str(Safe_Str__Python__Module('__internal__'       )) == '__internal__'

    def test_version_number_handling(self):                      # Test module names with versions
        assert str(Safe_Str__Python__Module('api_v1'             )) == 'api_v1'
        assert str(Safe_Str__Python__Module('api_v2'             )) == 'api_v2'
        assert str(Safe_Str__Python__Module('module_v1_0'        )) == 'module_v1_0'
        assert str(Safe_Str__Python__Module('lib_2024'           )) == 'lib_2024'

    def test_namespace_package_pattern(self):                    # Test namespace package naming
        # Namespace packages use underscores or dots
        assert str(Safe_Str__Python__Module('namespace_pkg'      )) == 'namespace_pkg'
        assert str(Safe_Str__Python__Module('com.example'        )) == 'com_example'                  # Dots become underscores

    def test_real_world_module_names(self):                      # Test actual Python module name patterns
        # From standard library
        assert str(Safe_Str__Python__Module('asyncio'            )) == 'asyncio'
        assert str(Safe_Str__Python__Module('collections'        )) == 'collections'
        assert str(Safe_Str__Python__Module('itertools'          )) == 'itertools'

        # From popular packages
        assert str(Safe_Str__Python__Module('numpy'              )) == 'numpy'
        assert str(Safe_Str__Python__Module('pandas'             )) == 'pandas'
        assert str(Safe_Str__Python__Module('requests'           )) == 'requests'

        # Project-specific
        assert str(Safe_Str__Python__Module('osbot_utils'        )) == 'osbot_utils'
        assert str(Safe_Str__Python__Module('type_safe'          )) == 'type_safe'

    def test_import_statement_compatibility(self):               # Test names work in import statements
        # These should all be valid module names
        valid_modules = [
            'utils', 'helpers', 'config', 'settings',
            'user_service', 'api_client', 'data_models',
            '_internal', '__main__', 'api_v1'
        ]

        for module_name in valid_modules:
            result = str(Safe_Str__Python__Module(module_name))
            assert result == module_name                                                              # Should be unchanged
            assert result.replace('_', '').replace('0', '').replace('1', '').replace('2', '').replace('3', '').replace('4', '').replace('5', '').replace('6', '').replace('7', '').replace('8', '').replace('9', '').isalpha() or result.startswith('_')