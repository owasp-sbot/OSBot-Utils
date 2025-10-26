import pytest
from unittest                                                                          import TestCase
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Authorization import Safe_Str__Http__Authorization


class test_Safe_Str__Http__Authorization(TestCase):

    def test__init__(self):                                                             # Test Safe_Str__Http__Authorization initialization
        auth = Safe_Str__Http__Authorization('Bearer token123')
        assert type(auth)             is Safe_Str__Http__Authorization
        assert str(auth)              == 'Bearer token123'
        assert auth                   == 'Bearer token123'

    def test__bearer_tokens(self):                                                      # Test Bearer token authentication
        assert Safe_Str__Http__Authorization('Bearer abc123def456') == 'Bearer abc123def456'
        assert Safe_Str__Http__Authorization('Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9') == 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
        assert Safe_Str__Http__Authorization('Bearer token-with-dashes') == 'Bearer token-with-dashes'
        assert Safe_Str__Http__Authorization('Bearer token_with_underscores') == 'Bearer token_with_underscores'

    def test__basic_authentication(self):                                               # Test Basic authentication scheme
        assert Safe_Str__Http__Authorization('Basic dXNlcjpwYXNz') == 'Basic dXNlcjpwYXNz'
        assert Safe_Str__Http__Authorization('Basic YWRtaW46c2VjcmV0') == 'Basic YWRtaW46c2VjcmV0'
        assert Safe_Str__Http__Authorization('Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==') == 'Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ=='

    def test__digest_authentication(self):                                              # Test Digest authentication scheme
        assert Safe_Str__Http__Authorization('Digest username="user", realm="realm"') == 'Digest username="user", realm="realm"'
        assert Safe_Str__Http__Authorization('Digest username="admin"') == 'Digest username="admin"'

    def test__api_key_authentication(self):                                             # Test API key authentication
        assert Safe_Str__Http__Authorization('ApiKey abc-123-def-456') == 'ApiKey abc-123-def-456'
        assert Safe_Str__Http__Authorization('ApiKey sk_live_1234567890') == 'ApiKey sk_live_1234567890'
        assert Safe_Str__Http__Authorization('X-API-Key my-secret-key') == 'X-API-Key my-secret-key'

    def test__oauth_tokens(self):                                                       # Test OAuth authentication
        assert Safe_Str__Http__Authorization('OAuth oauth_consumer_key="key"') == 'OAuth oauth_consumer_key="key"'
        assert Safe_Str__Http__Authorization('OAuth realm="Example"') == 'OAuth realm="Example"'

    def test__aws_signature(self):                                                      # Test AWS Signature authentication
        aws_sig = 'AWS4-HMAC-SHA256 Credential=AKIAIOSFODNN7EXAMPLE/20130524/us-east-1/s3/aws4_request, SignedHeaders=host;range;x-amz-date, Signature=abc123'
        assert Safe_Str__Http__Authorization(aws_sig           ) == aws_sig

    def test__jwt_tokens(self):                                                         # Test JWT token structure
        jwt = 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        assert Safe_Str__Http__Authorization(jwt               ) == jwt

    def test__whitespace_handling(self):                                                # Test trim_whitespace = True
        assert Safe_Str__Http__Authorization('  Bearer token123  ') == 'Bearer token123'
        assert Safe_Str__Http__Authorization('Basic dXNlcjpwYXNz  ') == 'Basic dXNlcjpwYXNz'
        assert Safe_Str__Http__Authorization('  ApiKey abc-123'  ) == 'ApiKey abc-123'

    def test__numeric_conversion(self):                                                 # Test conversion from numeric types
        assert Safe_Str__Http__Authorization(12345               ) == '12345'
        assert Safe_Str__Http__Authorization(999999              ) == '999999'

    def test__control_characters(self):                                                 # Control characters get replaced
        assert Safe_Str__Http__Authorization('Bearer\x00token'  ) == 'Bearer_token'
        assert Safe_Str__Http__Authorization('Basic\x01auth'    ) == 'Basic_auth'
        assert Safe_Str__Http__Authorization('ApiKey\x1Ftest'   ) == 'ApiKey_test'

    def test__empty_values(self):                                                       # Test allow_empty = False enforcement
        assert Safe_Str__Http__Authorization(None ) == ''
        assert Safe_Str__Http__Authorization(''   ) == ''
        assert Safe_Str__Http__Authorization('   ') == ''                               # Spaces only (will be trimmed)


    def test__max_length(self):                                                         # Test TYPE_SAFE_STR__HTTP__AUTHORIZATION__MAX_LENGTH = 2048
        valid_2048   = 'Bearer ' + 'a' * 2041                                           # 'Bearer ' = 7 chars + 2041 = 2048
        invalid_2049 = 'Bearer ' + 'a' * 2042

        assert Safe_Str__Http__Authorization(valid_2048          ) == valid_2048

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__Authorization(invalid_2049)
        assert "in Safe_Str__Http__Authorization, value exceeds maximum length of 2048" in str(exc_info.value)

    def test__long_tokens(self):                                                        # Test long bearer tokens
        long_token = 'Bearer ' + 'a' * 2000
        assert len(Safe_Str__Http__Authorization(long_token)     ) == len(long_token)

    def test__special_characters(self):                                                 # Test allowed special characters in auth values
        assert Safe_Str__Http__Authorization('Bearer token.with.dots') == 'Bearer token.with.dots'
        assert Safe_Str__Http__Authorization('Bearer token/with/slashes') == 'Bearer token/with/slashes'
        assert Safe_Str__Http__Authorization('Bearer token=with=equals') == 'Bearer token=with=equals'
        assert Safe_Str__Http__Authorization('Basic token+with+plus') == 'Basic token+with+plus'

    def test__str_and_repr(self):                                                       # Test string representations
        auth = Safe_Str__Http__Authorization('Bearer token123')

        assert str(auth)              == 'Bearer token123'
        assert f"{auth}"              == 'Bearer token123'
        assert f"Authorization: {auth}" == 'Authorization: Bearer token123'