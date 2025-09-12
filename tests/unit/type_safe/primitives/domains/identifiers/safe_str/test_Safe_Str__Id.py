import sys
import pytest
from unittest                                                                   import TestCase
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Str                             import Safe_Str
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id, TYPE_SAFE_STR__ID__MAX_LENGTH


class test_Safe_Str__Id(TestCase):

    def test__init__(self):                                      # Test basic initialization
        with Safe_Str__Id() as _:
            assert type(_)                      is Safe_Str__Id
            assert _.regex.pattern              == r'[^a-zA-Z0-9_\-]'        # Only alphanumerics, underscore, hyphen
            assert _.max_length                 == TYPE_SAFE_STR__ID__MAX_LENGTH
            assert _.allow_empty                is True
            assert _.trim_whitespace            is True
            assert _.allow_all_replacement_char is True

    def test_valid_ids(self):                                   # Test valid identifier patterns
        # Basic valid IDs
        assert str(Safe_Str__Id('user-123'        )) == 'user-123'
        assert str(Safe_Str__Id('order_456'       )) == 'order_456'
        assert str(Safe_Str__Id('my-identifier'   )) == 'my-identifier'
        assert str(Safe_Str__Id('my_identifier'   )) == 'my_identifier'
        assert str(Safe_Str__Id('ABC-123-DEF'     )) == 'ABC-123-DEF'

        # AWS-style IDs
        assert str(Safe_Str__Id('i-1234567890abcdef0'  )) == 'i-1234567890abcdef0'
        assert str(Safe_Str__Id('vol-0a1b2c3d4e5f'     )) == 'vol-0a1b2c3d4e5f'
        assert str(Safe_Str__Id('ami-12345678'         )) == 'ami-12345678'

        # Docker/Kubernetes style IDs
        assert str(Safe_Str__Id('container-name-1'     )) == 'container-name-1'
        assert str(Safe_Str__Id('my-pod-name'          )) == 'my-pod-name'
        assert str(Safe_Str__Id('service_v2_production')) == 'service_v2_production'

        # Database record IDs
        assert str(Safe_Str__Id('USR_2024_001'         )) == 'USR_2024_001'
        assert str(Safe_Str__Id('ORDER-2024-03-15-001' )) == 'ORDER-2024-03-15-001'

        # UUID-like patterns
        assert str(Safe_Str__Id('a1b2c3d4-e5f6-7890'   )) == 'a1b2c3d4-e5f6-7890'

        # Edge cases - empty and None
        assert str(Safe_Str__Id(None)) == ''
        assert str(Safe_Str__Id(''  )) == ''

    def test_sanitization(self):                                # Test character replacement
        # Special characters get replaced with underscore
        assert str(Safe_Str__Id('user@123'        )) == 'user_123'
        assert str(Safe_Str__Id('order#456'       )) == 'order_456'
        assert str(Safe_Str__Id('my.identifier'   )) == 'my_identifier'
        assert str(Safe_Str__Id('my identifier'   )) == 'my_identifier'          # Space replaced
        assert str(Safe_Str__Id('my/id\\path'     )) == 'my_id_path'
        assert str(Safe_Str__Id('id!@#$%^&*()'    )) == 'id__________'

        # Mixed valid and invalid characters
        assert str(Safe_Str__Id('user-123!@#'     )) == 'user-123___'
        assert str(Safe_Str__Id('order_456$%^'    )) == 'order_456___'
        assert str(Safe_Str__Id('id (version 2)'  )) == 'id__version_2_'
        assert str(Safe_Str__Id('2024/03/15-id'   )) == '2024_03_15-id'

        # Unicode characters
        assert str(Safe_Str__Id('café-123'        )) == 'caf_-123'
        assert str(Safe_Str__Id('résumé_001'      )) == 'r_sum__001'
        assert str(Safe_Str__Id('naïve-id'        )) == 'na_ve-id'
        assert str(Safe_Str__Id('🚀rocket-id'     )) == '_rocket-id'
        assert str(Safe_Str__Id('id-😀-happy'     )) == 'id-_-happy'

    def test_trimming(self):                                    # Test whitespace trimming
        assert str(Safe_Str__Id('  id-123  '      )) == 'id-123'
        assert str(Safe_Str__Id('\tid-456\t'      )) == 'id-456'
        assert str(Safe_Str__Id('\nid-789\n'      )) == 'id-789'
        assert str(Safe_Str__Id('  \t id_001 \n ' )) == 'id_001'

        # Multiple spaces become single underscore
        assert str(Safe_Str__Id('id   with   spaces')) == 'id___with___spaces'

    def test_max_length(self):                                  # Test length constraints
        # At max length - should pass
        max_id = 'a' * TYPE_SAFE_STR__ID__MAX_LENGTH
        assert str(Safe_Str__Id(max_id)) == max_id
        assert len(Safe_Str__Id(max_id)) == TYPE_SAFE_STR__ID__MAX_LENGTH

        # Exceeds max length - should raise
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Id('a' * (TYPE_SAFE_STR__ID__MAX_LENGTH + 1))
        assert f"value exceeds maximum length of {TYPE_SAFE_STR__ID__MAX_LENGTH}" in str(exc_info.value)

    def test_type_conversion(self):                             # Test conversion from other types
        # From integer
        assert str(Safe_Str__Id(123      )) == '123'
        assert str(Safe_Str__Id(0        )) == '0'

        # From float
        assert str(Safe_Str__Id(123.456  )) == '123_456'      # Dot becomes underscore

        # From boolean
        assert str(Safe_Str__Id(True     )) == 'True'
        assert str(Safe_Str__Id(False    )) == 'False'

        # From another Safe_Str
        other = Safe_Str('test-id')
        assert str(Safe_Str__Id(other)) == 'test_id'

    def test_concatenation(self):                               # Test string concatenation behavior
        id_val = Safe_Str__Id('user-123')

        # Concatenation returns regular string, not Safe_Str__Id
        result = id_val + '-suffix!'
        assert type(result) is Safe_Str__Id                     # didn't lost type safety
        assert result == 'user-123-suffix_'                     # where the sanitisation still occured

        result = '!prefix-' + id_val
        assert type(result) is Safe_Str__Id
        assert result == '_prefix-user-123'                     # same here

        # Using with format strings
        assert f"ID: {id_val}"         == "ID: user-123"
        assert "ID: {}".format(id_val) == "ID: user-123"

    def test_repr_and_str(self):                                # Test string representations
        id_val = Safe_Str__Id('test-id-123')

        assert str(id_val)  == 'test-id-123'
        assert repr(id_val) == "Safe_Str__Id('test-id-123')"

        # Empty ID
        empty = Safe_Str__Id('')
        assert str(empty)   == ''
        assert repr(empty)  == "Safe_Str__Id('')"

    def test_in_type_safe_schema(self):                         # Test usage in Type_Safe classes
        class Schema__Resource(Type_Safe):
            resource_id   : Safe_Str__Id
            container_id  : Safe_Str__Id
            deployment_id : Safe_Str__Id

        with Schema__Resource() as _:
            # Auto-initialization
            assert type(_.resource_id  ) is Safe_Str__Id
            assert type(_.container_id ) is Safe_Str__Id
            assert type(_.deployment_id) is Safe_Str__Id

            # Setting with raw strings (auto-conversion)
            _.resource_id = 'res-2024-001'
            assert _.resource_id == 'res-2024-001'

            # Setting with special chars (sanitization)
            _.container_id = 'container@prod#001'
            assert _.container_id == 'container_prod_001'

            # Setting with Safe_Str__Id
            _.deployment_id = Safe_Str__Id('deploy-v2-stable')
            assert _.deployment_id == 'deploy-v2-stable'

            # JSON serialization
            json_data = _.json()
            assert json_data['resource_id'  ] == 'res-2024-001'
            assert json_data['container_id' ] == 'container_prod_001'
            assert json_data['deployment_id'] == 'deploy-v2-stable'

    def test_common_id_patterns(self):                          # Test real-world ID patterns
        # GitHub Actions run ID
        assert str(Safe_Str__Id('run-1234567890')) == 'run-1234567890'

        # Jira ticket ID
        assert str(Safe_Str__Id('PROJ-1234'     )) == 'PROJ-1234'

        # Semantic version tag
        assert str(Safe_Str__Id('v1_2_3-alpha'  )) == 'v1_2_3-alpha'

        # Build ID
        assert str(Safe_Str__Id('build-2024-03-15-001')) == 'build-2024-03-15-001'

        # Session ID
        assert str(Safe_Str__Id('sess_abc123def456'  )) == 'sess_abc123def456'

        # API key prefix (not the full key)
        assert str(Safe_Str__Id('sk-proj-123'        )) == 'sk-proj-123'

    def test_edge_cases(self):                                  # Test edge cases and corner scenarios
        # Only hyphens
        assert str(Safe_Str__Id('---'           )) == '---'

        # Only underscores
        assert str(Safe_Str__Id('___'           )) == '___'

        # Mix of valid separators
        assert str(Safe_Str__Id('-_-_-'         )) == '-_-_-'

        # Numbers only
        assert str(Safe_Str__Id('123456789'     )) == '123456789'

        # Single character
        assert str(Safe_Str__Id('a'             )) == 'a'
        assert str(Safe_Str__Id('1'             )) == '1'
        assert str(Safe_Str__Id('-'             )) == '-'
        assert str(Safe_Str__Id('_'             )) == '_'

        # Start/end with separators (valid for IDs)
        assert str(Safe_Str__Id('-id-'          )) == '-id-'
        assert str(Safe_Str__Id('_id_'          )) == '_id_'
        assert str(Safe_Str__Id('-_id_-'        )) == '-_id_-'