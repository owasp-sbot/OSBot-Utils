import pytest
from unittest                                                                            import TestCase
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Header__Name import Safe_Str__Http__Header__Name


class test_Safe_Str__Http__Header__Name(TestCase):

    def test__init__(self):                                                             # Test Safe_Str__Http__Header__Name initialization
        header_name = Safe_Str__Http__Header__Name('Content-Type')
        assert type(header_name)      is Safe_Str__Http__Header__Name
        assert str(header_name)       == 'content-type'                                 # Converted to lowercase
        assert header_name            == 'content-type'

    def test__standard_header_names(self):                                              # Test common HTTP header names per RFC 7230
        assert Safe_Str__Http__Header__Name('Content-Type'        ) == 'content-type'
        assert Safe_Str__Http__Header__Name('Authorization'       ) == 'authorization'
        assert Safe_Str__Http__Header__Name('User-Agent'          ) == 'user-agent'
        assert Safe_Str__Http__Header__Name('Accept'              ) == 'accept'
        assert Safe_Str__Http__Header__Name('Cache-Control'       ) == 'cache-control'
        assert Safe_Str__Http__Header__Name('Accept-Encoding'     ) == 'accept-encoding'
        assert Safe_Str__Http__Header__Name('Accept-Language'     ) == 'accept-language'
        assert Safe_Str__Http__Header__Name('If-None-Match'       ) == 'if-none-match'
        assert Safe_Str__Http__Header__Name('If-Modified-Since'   ) == 'if-modified-since'
        assert Safe_Str__Http__Header__Name('Content-Length'      ) == 'content-length'
        assert Safe_Str__Http__Header__Name('Content-Encoding'    ) == 'content-encoding'
        assert Safe_Str__Http__Header__Name('Transfer-Encoding'   ) == 'transfer-encoding'
        assert Safe_Str__Http__Header__Name('Connection'          ) == 'connection'
        assert Safe_Str__Http__Header__Name('Host'                ) == 'host'
        assert Safe_Str__Http__Header__Name('Referer'             ) == 'referer'
        assert Safe_Str__Http__Header__Name('Origin'              ) == 'origin'

    def test__custom_headers(self):                                                     # Test custom X- prefixed headers
        assert Safe_Str__Http__Header__Name('X-Request-ID'        ) == 'x-request-id'
        assert Safe_Str__Http__Header__Name('X-API-Key'           ) == 'x-api-key'
        assert Safe_Str__Http__Header__Name('X-Forwarded-For'     ) == 'x-forwarded-for'
        assert Safe_Str__Http__Header__Name('X-Forwarded-Proto'   ) == 'x-forwarded-proto'
        assert Safe_Str__Http__Header__Name('X-Forwarded-Host'    ) == 'x-forwarded-host'
        assert Safe_Str__Http__Header__Name('X-Real-IP'           ) == 'x-real-ip'
        assert Safe_Str__Http__Header__Name('X-Correlation-ID'    ) == 'x-correlation-id'
        assert Safe_Str__Http__Header__Name('X-Custom-Header'     ) == 'x-custom-header'

    def test__alphanumeric_names(self):                                                 # Test headers with numbers
        assert Safe_Str__Http__Header__Name('Header123'           ) == 'header123'
        assert Safe_Str__Http__Header__Name('Content-Type-V2'     ) == 'content-type-v2'
        assert Safe_Str__Http__Header__Name('API-Version-2'       ) == 'api-version-2'
        assert Safe_Str__Http__Header__Name('X-RateLimit-Limit'   ) == 'x-ratelimit-limit'
        assert Safe_Str__Http__Header__Name('X-RateLimit-Remaining') == 'x-ratelimit-remaining'

    def test__lowercase_conversion(self):                                               # HTTP/2 and HTTP/3 require lowercase per RFC 7540 and RFC 9114
        assert Safe_Str__Http__Header__Name('content-type'        ) == 'content-type'
        assert Safe_Str__Http__Header__Name('CONTENT-TYPE'        ) == 'content-type'
        assert Safe_Str__Http__Header__Name('Content-Type'        ) == 'content-type'
        assert Safe_Str__Http__Header__Name('CoNtEnT-TyPe'        ) == 'content-type'
        assert Safe_Str__Http__Header__Name('USER-AGENT'          ) == 'user-agent'
        assert Safe_Str__Http__Header__Name('User-Agent'          ) == 'user-agent'

    def test__whitespace_handling(self):                                                # Test trim_whitespace = True
        assert Safe_Str__Http__Header__Name('  Content-Type  '    ) == 'content-type'
        assert Safe_Str__Http__Header__Name('Authorization  '     ) == 'authorization'
        assert Safe_Str__Http__Header__Name('  X-API-Key'         ) == 'x-api-key'
        assert Safe_Str__Http__Header__Name('\tContent-Type\t'    ) == 'content-type'
        assert Safe_Str__Http__Header__Name('\nAuthorization\n'   ) == 'authorization'

    def test__numeric_conversion(self):                                                 # Test conversion from numeric types
        assert Safe_Str__Http__Header__Name(12345                 ) == '12345'
        assert Safe_Str__Http__Header__Name(0                     ) == '0'
        assert Safe_Str__Http__Header__Name(999                   ) == '999'

    def test__invalid_characters(self):                                                 # Test regex character replacement
        assert Safe_Str__Http__Header__Name('Content_Type'        ) == 'content_type'       # Underscore invalid in RFC 7230
        assert Safe_Str__Http__Header__Name('Content/Type'        ) == 'content_type'
        assert Safe_Str__Http__Header__Name('Content:Type'        ) == 'content_type'
        assert Safe_Str__Http__Header__Name('Content Type'        ) == 'content_type'       # Space replaced
        assert Safe_Str__Http__Header__Name('Content@Type'        ) == 'content_type'
        assert Safe_Str__Http__Header__Name('Content.Type'        ) == 'content_type'
        assert Safe_Str__Http__Header__Name('Content+Type'        ) == 'content_type'
        assert Safe_Str__Http__Header__Name('Content=Type'        ) == 'content_type'
        assert Safe_Str__Http__Header__Name('Content;Type'        ) == 'content_type'
        assert Safe_Str__Http__Header__Name('Content,Type'        ) == 'content_type'

    def test__special_characters(self):                                                 # Test various special character combinations
        assert Safe_Str__Http__Header__Name('Header!@#$%^'        ) == 'header______'
        assert Safe_Str__Http__Header__Name('Test<>Header'        ) == 'test__header'
        assert Safe_Str__Http__Header__Name('Header[]{}'          ) == 'header____'

    def test__empty_values(self):                                                       # Test allow_empty = True for JSON roundtripping
        assert Safe_Str__Http__Header__Name(None                  ) == ''
        assert Safe_Str__Http__Header__Name(''                    ) == ''
        assert Safe_Str__Http__Header__Name('   '                 ) == ''                # Spaces only (will be trimmed)

    def test__all_invalid_characters(self):                                             # Test string with only invalid chars becomes empty
        assert Safe_Str__Http__Header__Name('<?&*^?>'             ) == '_______'
        assert Safe_Str__Http__Header__Name('!@#$%^&*()'          ) == '__________'

    def test__max_length(self):                                                         # Test TYPE_SAFE_STR__HTTP__HEADER_NAME__MAX_LENGTH = 128
        valid_128   = 'a' * 128
        invalid_129 = 'a' * 129

        assert Safe_Str__Http__Header__Name(valid_128             ) == valid_128

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__Header__Name(invalid_129)
        assert "in Safe_Str__Http__Header__Name, value exceeds maximum length of 128" in str(exc_info.value)

    def test__real_world_headers(self):                                                 # Test real HTTP header names from various APIs
        # AWS headers
        assert Safe_Str__Http__Header__Name('X-Amz-Date'          ) == 'x-amz-date'
        assert Safe_Str__Http__Header__Name('X-Amz-Content-Sha256') == 'x-amz-content-sha256'

        # Security headers
        assert Safe_Str__Http__Header__Name('Strict-Transport-Security') == 'strict-transport-security'
        assert Safe_Str__Http__Header__Name('Content-Security-Policy'  ) == 'content-security-policy'
        assert Safe_Str__Http__Header__Name('X-Content-Type-Options'   ) == 'x-content-type-options'
        assert Safe_Str__Http__Header__Name('X-Frame-Options'          ) == 'x-frame-options'
        assert Safe_Str__Http__Header__Name('X-XSS-Protection'         ) == 'x-xss-protection'

        # CORS headers
        assert Safe_Str__Http__Header__Name('Access-Control-Allow-Origin'     ) == 'access-control-allow-origin'
        assert Safe_Str__Http__Header__Name('Access-Control-Allow-Methods'    ) == 'access-control-allow-methods'
        assert Safe_Str__Http__Header__Name('Access-Control-Allow-Headers'    ) == 'access-control-allow-headers'
        assert Safe_Str__Http__Header__Name('Access-Control-Allow-Credentials') == 'access-control-allow-credentials'

    def test__http2_compliance(self):                                                   # Test HTTP/2 and HTTP/3 lowercase requirement
        # RFC 7540 Section 8.1.2: header field names MUST be converted to lowercase
        mixed_case_headers = [
            ('Content-Type', 'content-type'),
            ('AUTHORIZATION', 'authorization'),
            ('User-Agent', 'user-agent'),
            ('X-Request-ID', 'x-request-id'),
            ('Cache-CONTROL', 'cache-control'),
        ]

        for input_val, expected in mixed_case_headers:
            assert Safe_Str__Http__Header__Name(input_val         ) == expected

    def test__str_and_repr(self):                                                       # Test string representations
        header_name = Safe_Str__Http__Header__Name('Content-Type')

        assert str(header_name)       == 'content-type'
        assert f"{header_name}"       == 'content-type'
        assert f"Header: {header_name}" == 'Header: content-type'