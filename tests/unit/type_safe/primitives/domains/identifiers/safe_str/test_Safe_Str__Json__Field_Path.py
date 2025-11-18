import re
import pytest
from unittest                                                                                 import TestCase
from osbot_utils.type_safe.Type_Safe                                                          import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Json__Field_Path import Safe_Str__Json__Field_Path
from osbot_utils.utils.Objects                                                                import base_classes
from osbot_utils.type_safe.Type_Safe__Primitive                                               import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.core.Safe_Str                                           import Safe_Str



class test_Safe_Str__Json__Field_Path(TestCase):

    def test__init__(self):                                                               # Test basic initialization
        field_path = Safe_Str__Json__Field_Path("user.profile.name")

        assert type(field_path) is Safe_Str__Json__Field_Path
        assert base_classes(field_path) == [Safe_Str, Type_Safe__Primitive, str, object, object]

        # Verify attributes
        assert field_path          == "user.profile.name"
        assert field_path.max_length == 256                                               # Longer for deep nesting
        assert field_path.trim_whitespace is True

    def test__init__empty(self):                                                          # Test empty initialization
        field_path = Safe_Str__Json__Field_Path()

        assert field_path == ''
        assert type(field_path) is Safe_Str__Json__Field_Path

    def test_simple_field_names(self):                                                    # Test basic field names
        field_path = Safe_Str__Json__Field_Path("username")
        assert field_path == "username"

        field_path = Safe_Str__Json__Field_Path("email_address")
        assert field_path == "email_address"

        field_path = Safe_Str__Json__Field_Path("user-id")
        assert field_path == "user-id"

    def test_nested_field_paths(self):                                                    # Test dot-separated nesting
        field_path = Safe_Str__Json__Field_Path("user.name")
        assert field_path == "user.name"

        field_path = Safe_Str__Json__Field_Path("config.database.connection.timeout")
        assert field_path == "config.database.connection.timeout"

        # Deep nesting
        field_path = Safe_Str__Json__Field_Path("a.b.c.d.e.f.g.h")
        assert field_path == "a.b.c.d.e.f.g.h"

    def test_allowed_characters(self):                                                    # Test valid character set
        # Alphanumeric
        field_path = Safe_Str__Json__Field_Path("field123")
        assert field_path == "field123"

        # Underscores
        field_path = Safe_Str__Json__Field_Path("user_name")
        assert field_path == "user_name"

        # Hyphens
        field_path = Safe_Str__Json__Field_Path("user-name")
        assert field_path == "user-name"

        # Dots for nesting
        field_path = Safe_Str__Json__Field_Path("user.profile")
        assert field_path == "user.profile"

        # Mixed
        field_path = Safe_Str__Json__Field_Path("user_data.profile-info.name123")
        assert field_path == "user_data.profile-info.name123"

    def test_consecutive_dots_rejected(self):                                             # Test consecutive dots not allowed
        error_message = "Field path cannot contain consecutive dots: 'user..name'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__Json__Field_Path("user..name")

        error_message = "Field path cannot contain consecutive dots: 'config...database'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__Json__Field_Path("config...database")

    def test_leading_dot_rejected(self):                                                  # Test leading dots not allowed
        error_message = "Field path cannot start or end with a dot: '.username'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__Json__Field_Path(".username")

        error_message = "Field path cannot start or end with a dot: '.user.profile'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__Json__Field_Path(".user.profile")

    def test_trailing_dot_rejected(self):                                                 # Test trailing dots not allowed
        error_message = "Field path cannot start or end with a dot: 'username.'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__Json__Field_Path("username.")

        error_message = "Field path cannot start or end with a dot: 'user.profile.'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__Json__Field_Path("user.profile.")

    def test_empty_segments_rejected(self):                                               # Test empty path segments not allowed
        # Consecutive dots create empty segments
        error_message = "Field path cannot contain consecutive dots: 'user..profile'"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__Json__Field_Path("user..profile")

    def test_invalid_characters_sanitized(self):                                          # Test special characters sanitized
        # Spaces replaced
        field_path = Safe_Str__Json__Field_Path("user name")
        assert field_path == "user_name"

        # Special characters replaced
        field_path = Safe_Str__Json__Field_Path("user@profile")
        assert field_path == "user_profile"

        # Multiple special chars
        field_path = Safe_Str__Json__Field_Path("user!@#$%profile")
        assert field_path == "user_____profile"

        # Dots preserved for nesting
        field_path = Safe_Str__Json__Field_Path("user@email.domain!com")
        assert field_path == "user_email.domain_com"

    def test_whitespace_trimming(self):                                                   # Test whitespace trimming
        field_path = Safe_Str__Json__Field_Path("  username  ")
        assert field_path == "username"

        field_path = Safe_Str__Json__Field_Path("  user.profile  ")
        assert field_path == "user.profile"

        # Internal whitespace replaced
        field_path = Safe_Str__Json__Field_Path("user name")
        assert field_path == "user_name"

    def test_max_length_enforcement(self):                                                # Test 256 character limit
        # At limit
        long_path = "a" * 256
        field_path = Safe_Str__Json__Field_Path(long_path)
        assert len(field_path) == 256

        # Exceeds limit
        too_long = "a" * 257
        with pytest.raises(ValueError):
            Safe_Str__Json__Field_Path(too_long)

    def test_deep_nesting_scenarios(self):                                                # Test realistic deep nesting
        # API response path
        field_path = Safe_Str__Json__Field_Path("response.data.user.profile.settings.theme.color")
        assert field_path == "response.data.user.profile.settings.theme.color"

        # Database schema path
        field_path = Safe_Str__Json__Field_Path("schema.tables.users.columns.email.validators.format")
        assert field_path == "schema.tables.users.columns.email.validators.format"

        # JSON path
        field_path = Safe_Str__Json__Field_Path("root.items.0.attributes.metadata.tags")
        assert field_path == "root.items.0.attributes.metadata.tags"

    def test_context_manager(self):                                                       # Test context manager support
        with Safe_Str__Json__Field_Path("user.profile") as field_path:
            assert field_path == "user.profile"
            assert type(field_path) is Safe_Str__Json__Field_Path

    def test_string_operations(self):                                                     # Test string method compatibility
        field_path = Safe_Str__Json__Field_Path("user.profile.name")

        # Split works
        segments = field_path.split('.')
        assert segments == ['user', 'profile', 'name']

        # Startswith works
        assert field_path.startswith('user')
        assert not field_path.startswith('profile')

        # Endswith works
        assert field_path.endswith('name')
        assert not field_path.endswith('user')

        # Length works
        assert field_path      == 'user.profile.name'
        assert len(field_path) == 17


    def test_common_database_field_paths(self):                                           # Test typical database scenarios
        # Table.column
        field_path = Safe_Str__Json__Field_Path("users.email")
        assert field_path == "users.email"

        # Schema.table.column
        field_path = Safe_Str__Json__Field_Path("public.users.created_at")
        assert field_path == "public.users.created_at"

        # Join path
        field_path = Safe_Str__Json__Field_Path("users.orders.items.product_id")
        assert field_path == "users.orders.items.product_id"

    def test_common_json_field_paths(self):                                               # Test typical JSON scenarios
        # Simple nested
        field_path = Safe_Str__Json__Field_Path("data.results")
        assert field_path == "data.results"

        # Array access style
        field_path = Safe_Str__Json__Field_Path("items.0.attributes")
        assert field_path == "items.0.attributes"

        # Deep object path
        field_path = Safe_Str__Json__Field_Path("response.body.data.user.preferences.notifications.email")
        assert field_path == "response.body.data.user.preferences.notifications.email"

    def test_config_file_paths(self):                                                     # Test configuration file paths
        # YAML-style path
        field_path = Safe_Str__Json__Field_Path("database.connection.host")
        assert field_path == "database.connection.host"

        # Application config
        field_path = Safe_Str__Json__Field_Path("app.logging.level")
        assert field_path == "app.logging.level"

        # Feature flags
        field_path = Safe_Str__Json__Field_Path("features.authentication.oauth.enabled")
        assert field_path == "features.authentication.oauth.enabled"

    def test_edge_cases(self):                                                            # Test edge case scenarios
        # Single character
        field_path = Safe_Str__Json__Field_Path("x")
        assert field_path == "x"

        # Single character segments
        field_path = Safe_Str__Json__Field_Path("a.b.c")
        assert field_path == "a.b.c"

        # Numbers only
        field_path = Safe_Str__Json__Field_Path("123")
        assert field_path == "123"

        # Mixed case preserved
        field_path = Safe_Str__Json__Field_Path("User.Profile.Name")
        assert field_path == "User.Profile.Name"

    def test_comparison_operations(self):                                                 # Test equality and comparison
        path1 = Safe_Str__Json__Field_Path("user.name")
        path2 = Safe_Str__Json__Field_Path("user.name")
        path3 = Safe_Str__Json__Field_Path("user.email")

        # Equality
        assert path1 == path2
        assert path1 != path3

        # String comparison
        assert path1 == "user.name"
        assert path1 != "user.email"

    def test_regex_pattern(self):                                                         # Test underlying regex pattern
        # Pattern should reject special chars except dots, hyphens, underscores
        field_path = Safe_Str__Json__Field_Path("valid-field_name123.nested")
        assert field_path == "valid-field_name123.nested"

        # Special chars get replaced
        field_path = Safe_Str__Json__Field_Path("invalid@field#name")
        assert field_path == "invalid_field_name"

    def test_use_in_type_safe_class(self):                                                # Test usage in Type_Safe schema

        class Schema__Field_Config(Type_Safe):
            field_path  : Safe_Str__Json__Field_Path
            description : str

        config = Schema__Field_Config(field_path  = "user.profile.email",
                                      description = "User email field"  )

        assert type(config.field_path) is Safe_Str__Json__Field_Path
        assert config.field_path == "user.profile.email"

        # Auto-conversion works
        config.field_path = "user.name"
        assert type(config.field_path) is Safe_Str__Json__Field_Path
        assert config.field_path == "user.name"

    def test_serialization(self):                                                         # Test JSON serialization
        class Schema__Path_Config(Type_Safe):
            path: Safe_Str__Json__Field_Path

        config = Schema__Path_Config(path="user.profile.name")

        # Serialize
        json_data = config.json()
        assert json_data['path'] == "user.profile.name"

        # Deserialize
        restored = Schema__Path_Config.from_json(json_data)
        assert type(restored.path) is Safe_Str__Json__Field_Path
        assert restored.path == "user.profile.name"

    def test_none_handling(self):                                                         # Test None value handling
        # None converts to empty string
        field_path = Safe_Str__Json__Field_Path(None)
        assert field_path == ''

        # Empty string is valid
        field_path = Safe_Str__Json__Field_Path('')
        assert field_path == ''

    def test_concat_keeps_type(self):
        an_field_1   = Safe_Str__Json__Field_Path("user.preferences")
        an_field_2 = "data." + an_field_1
        an_field_3 = an_field_2 + ".notifications.email"


        assert an_field_1 == "user.preferences"
        assert an_field_2 == "data.user.preferences"
        assert an_field_3 == "data.user.preferences.notifications.email"
        assert type(an_field_1) is Safe_Str__Json__Field_Path
        assert type(an_field_2) is Safe_Str__Json__Field_Path
        assert type(an_field_3) is Safe_Str__Json__Field_Path