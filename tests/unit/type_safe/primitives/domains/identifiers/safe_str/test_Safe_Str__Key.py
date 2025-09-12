import pytest
from unittest                                                                    import TestCase
from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id  import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key import Safe_Str__Key


class test_Safe_Str__Key(TestCase):

    def test__init__(self):                                      # Test basic initialization
        with Safe_Str__Key() as _:
            assert type(_)                      is Safe_Str__Key
            assert _.regex.pattern              == r'[^a-zA-Z0-9_.-]'        # Allows alphanumerics, underscore, dot, hyphen
            assert _.allow_empty                is True
            assert _.trim_whitespace            is True
            assert _.allow_all_replacement_char is True

    def test_valid_keys(self):                                  # Test valid key patterns
        # Basic configuration keys
        assert str(Safe_Str__Key('api_key'              )) == 'api_key'
        assert str(Safe_Str__Key('API_KEY'              )) == 'API_KEY'
        assert str(Safe_Str__Key('database.host'        )) == 'database.host'
        assert str(Safe_Str__Key('database.port'        )) == 'database.port'
        assert str(Safe_Str__Key('user_id'              )) == 'user_id'
        assert str(Safe_Str__Key('session-token'        )) == 'session-token'

        # Dotted notation (hierarchical)
        assert str(Safe_Str__Key('app.module.setting'   )) == 'app.module.setting'
        assert str(Safe_Str__Key('service.api.endpoint' )) == 'service.api.endpoint'
        assert str(Safe_Str__Key('config.db.connection' )) == 'config.db.connection'
        assert str(Safe_Str__Key('logging.level.debug'  )) == 'logging.level.debug'

        # Environment variable style
        assert str(Safe_Str__Key('NODE_ENV'             )) == 'NODE_ENV'
        assert str(Safe_Str__Key('DATABASE_URL'         )) == 'DATABASE_URL'
        assert str(Safe_Str__Key('REDIS_HOST'           )) == 'REDIS_HOST'
        assert str(Safe_Str__Key('JWT_SECRET'           )) == 'JWT_SECRET'

        # Mixed formats
        assert str(Safe_Str__Key('aws.s3.bucket-name'   )) == 'aws.s3.bucket-name'
        assert str(Safe_Str__Key('feature.flag.v2'      )) == 'feature.flag.v2'
        assert str(Safe_Str__Key('cache.ttl.seconds'    )) == 'cache.ttl.seconds'
        assert str(Safe_Str__Key('retry.max-attempts'   )) == 'retry.max-attempts'

        # Numeric keys
        assert str(Safe_Str__Key('port_8080'            )) == 'port_8080'
        assert str(Safe_Str__Key('v1.2.3'               )) == 'v1.2.3'
        assert str(Safe_Str__Key('timeout_30s'          )) == 'timeout_30s'

        # Edge cases
        assert str(Safe_Str__Key(None)) == ''
        assert str(Safe_Str__Key(''  )) == ''

    def test_dots_allowed(self):                                # Test that dots work properly
        # Single dots
        assert str(Safe_Str__Key('a.b'                  )) == 'a.b'
        assert str(Safe_Str__Key('one.two.three'        )) == 'one.two.three'

        # Multiple consecutive dots (valid for keys)
        assert str(Safe_Str__Key('a..b'                 )) == 'a..b'
        assert str(Safe_Str__Key('...'                  )) == '...'

        # Starting/ending with dots
        assert str(Safe_Str__Key('.hidden'              )) == '.hidden'
        assert str(Safe_Str__Key('trailing.'            )) == 'trailing.'
        assert str(Safe_Str__Key('.both.'               )) == '.both.'

        # Common dotted patterns
        assert str(Safe_Str__Key('1.0.0'                )) == '1.0.0'
        assert str(Safe_Str__Key('127.0.0.1'            )) == '127.0.0.1'  # IP-like
        assert str(Safe_Str__Key('file.backup.tar.gz'   )) == 'file.backup.tar.gz'

    def test_hyphens_allowed(self):                             # Test that hyphens work properly
        # Single hyphens
        assert str(Safe_Str__Key('a-b'                  )) == 'a-b'
        assert str(Safe_Str__Key('one-two-three'        )) == 'one-two-three'

        # Multiple consecutive hyphens
        assert str(Safe_Str__Key('a--b'                 )) == 'a--b'
        assert str(Safe_Str__Key('---'                  )) == '---'

        # Starting/ending with hyphens
        assert str(Safe_Str__Key('-start'               )) == '-start'
        assert str(Safe_Str__Key('end-'                 )) == 'end-'
        assert str(Safe_Str__Key('-both-'               )) == '-both-'

        # Kebab-case patterns
        assert str(Safe_Str__Key('my-config-key'        )) == 'my-config-key'
        assert str(Safe_Str__Key('feature-flag-enabled' )) == 'feature-flag-enabled'

    def test_mixed_separators(self):                            # Test combinations of allowed separators
        assert str(Safe_Str__Key('app.env-prod'         )) == 'app.env-prod'
        assert str(Safe_Str__Key('api_v2.endpoint'      )) == 'api_v2.endpoint'
        assert str(Safe_Str__Key('service-name.config'  )) == 'service-name.config'
        assert str(Safe_Str__Key('db_host-primary'      )) == 'db_host-primary'
        assert str(Safe_Str__Key('a.b-c_d'              )) == 'a.b-c_d'
        assert str(Safe_Str__Key('_.-'                  )) == '_.-'

    def test_sanitization(self):                                # Test character replacement
        # Spaces replaced
        assert str(Safe_Str__Key('my key'               )) == 'my_key'
        assert str(Safe_Str__Key('database host'        )) == 'database_host'

        # Special characters replaced
        assert str(Safe_Str__Key('api@key'              )) == 'api_key'
        assert str(Safe_Str__Key('config#1'             )) == 'config_1'
        assert str(Safe_Str__Key('user:password'        )) == 'user_password'
        assert str(Safe_Str__Key('path/to/config'       )) == 'path_to_config'
        assert str(Safe_Str__Key('key=value'            )) == 'key_value'
        assert str(Safe_Str__Key('item[0]'              )) == 'item_0_'

        # Unicode replaced
        assert str(Safe_Str__Key('café_config'          )) == 'caf__config'
        assert str(Safe_Str__Key('résumé_key'           )) == 'r_sum__key'
        assert str(Safe_Str__Key('naïve.setting'        )) == 'na_ve.setting'

        # Mixed valid and invalid
        assert str(Safe_Str__Key('my.key@2024'          )) == 'my.key_2024'
        assert str(Safe_Str__Key('api-key#v2'           )) == 'api-key_v2'
        assert str(Safe_Str__Key('config (prod)'        )) == 'config__prod_'

    def test_trimming(self):                                    # Test whitespace trimming
        assert str(Safe_Str__Key('  api_key  '          )) == 'api_key'
        assert str(Safe_Str__Key('\tconfig.value\t'     )) == 'config.value'
        assert str(Safe_Str__Key('\n database.host \n'  )) == 'database.host'
        assert str(Safe_Str__Key('  \t key_name \n '    )) == 'key_name'

    def test_type_conversion(self):                             # Test conversion from other types
        # From integer
        assert str(Safe_Str__Key(123      )) == '123'
        assert str(Safe_Str__Key(0        )) == '0'

        # From float (dot preserved)
        assert str(Safe_Str__Key(123.456  )) == '123.456'
        assert str(Safe_Str__Key(1.0      )) == '1.0'

        # From boolean
        assert str(Safe_Str__Key(True     )) == 'True'
        assert str(Safe_Str__Key(False    )) == 'False'

    def test_in_type_safe_schema(self):                         # Test usage in Type_Safe classes
        class Schema__Config(Type_Safe):
            db_key      : Safe_Str__Key
            api_key     : Safe_Str__Key
            cache_key   : Safe_Str__Key

        with Schema__Config() as _:
            # Auto-initialization
            assert type(_.db_key   ) is Safe_Str__Key
            assert type(_.api_key  ) is Safe_Str__Key
            assert type(_.cache_key) is Safe_Str__Key

            # Setting with raw strings
            _.db_key = 'database.primary.host'
            assert _.db_key == 'database.primary.host'

            # Setting with special chars (sanitization)
            _.api_key = 'API_KEY:production'
            assert _.api_key == 'API_KEY_production'

            # Setting with Safe_Str__Key
            _.cache_key = Safe_Str__Key('cache.ttl.seconds')
            assert _.cache_key == 'cache.ttl.seconds'

            # JSON serialization
            json_data = _.json()
            assert json_data['db_key'   ] == 'database.primary.host'
            assert json_data['api_key'  ] == 'API_KEY_production'
            assert json_data['cache_key'] == 'cache.ttl.seconds'

    def test_common_config_patterns(self):                      # Test real-world configuration patterns
        # AWS configuration
        assert str(Safe_Str__Key('aws.region'           )) == 'aws.region'
        assert str(Safe_Str__Key('aws.access_key_id'    )) == 'aws.access_key_id'
        assert str(Safe_Str__Key('s3.bucket.name'       )) == 's3.bucket.name'

        # Database configuration
        assert str(Safe_Str__Key('db.host'              )) == 'db.host'
        assert str(Safe_Str__Key('db.port'              )) == 'db.port'
        assert str(Safe_Str__Key('postgres.max_connections')) == 'postgres.max_connections'
        assert str(Safe_Str__Key('redis.connection.timeout')) == 'redis.connection.timeout'

        # Application settings
        assert str(Safe_Str__Key('app.name'             )) == 'app.name'
        assert str(Safe_Str__Key('app.version'          )) == 'app.version'
        assert str(Safe_Str__Key('feature.new-ui.enabled')) == 'feature.new-ui.enabled'
        assert str(Safe_Str__Key('logging.level'        )) == 'logging.level'

        # API keys and secrets
        assert str(Safe_Str__Key('jwt.secret'           )) == 'jwt.secret'
        assert str(Safe_Str__Key('oauth.client_id'      )) == 'oauth.client_id'
        assert str(Safe_Str__Key('stripe.api_key'       )) == 'stripe.api_key'
        assert str(Safe_Str__Key('sendgrid.api-key'     )) == 'sendgrid.api-key'

    def test_edge_cases(self):                                  # Test edge cases
        # Only dots
        assert str(Safe_Str__Key('.'                    )) == '.'
        assert str(Safe_Str__Key('..'                   )) == '..'
        assert str(Safe_Str__Key('...'                  )) == '...'

        # Only hyphens
        assert str(Safe_Str__Key('-'                    )) == '-'
        assert str(Safe_Str__Key('--'                   )) == '--'
        assert str(Safe_Str__Key('---'                  )) == '---'

        # Only underscores
        assert str(Safe_Str__Key('_'                    )) == '_'
        assert str(Safe_Str__Key('__'                   )) == '__'
        assert str(Safe_Str__Key('___'                  )) == '___'

        # Complex separator patterns
        assert str(Safe_Str__Key('.-_'                  )) == '.-_'
        assert str(Safe_Str__Key('_.-._.-'              )) == '_.-._.-'
        assert str(Safe_Str__Key('a.b-c_d.e-f_g'        )) == 'a.b-c_d.e-f_g'

    def test_max_length(self):                                  # Test length constraints
        # Should inherit max_length from Safe_Str__Id (128)
        max_length = 128
        max_key = 'a' * max_length
        assert str(Safe_Str__Key(max_key)) == max_key
        assert len(Safe_Str__Key(max_key)) == max_length

        # Exceeds max length
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Key('a' * (max_length + 1))
        assert f"value exceeds maximum length of {max_length}" in str(exc_info.value)

    def test_difference_from_safe_id(self):                     # Compare with parent Safe_Str__Id
        test_string = 'config.database.host'

        # Safe_Str__Key preserves dots
        key = Safe_Str__Key(test_string)
        assert str(key) == 'config.database.host'              # Dots preserved

        # Safe_Str__Id would replace dots
        id_val = Safe_Str__Id(test_string)
        assert str(id_val) == 'config_database_host'           # Dots replaced

        # This distinction is important for:
        # - Hierarchical configuration keys
        # - Dotted notation in settings
        # - Namespace separation