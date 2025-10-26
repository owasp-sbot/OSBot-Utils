import pytest
from unittest                                                                           import TestCase
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Header__Value import Safe_Str__Http__Header__Value


class test_Safe_Str__Http__Header__Value(TestCase):

    def test__init__(self):                                                             # Test Safe_Str__Http__Header__Value initialization
        header_value = Safe_Str__Http__Header__Value('application/json')
        assert type(header_value)     is Safe_Str__Http__Header__Value
        assert str(header_value)      == 'application/json'
        assert header_value           == 'application/json'

    def test__standard_header_values(self):                                             # Test common header value formats
        assert Safe_Str__Http__Header__Value('application/json'   ) == 'application/json'
        assert Safe_Str__Http__Header__Value('text/html'          ) == 'text/html'
        assert Safe_Str__Http__Header__Value('Bearer token123'    ) == 'Bearer token123'
        assert Safe_Str__Http__Header__Value('max-age=3600'       ) == 'max-age=3600'
        assert Safe_Str__Http__Header__Value('gzip, deflate, br'  ) == 'gzip, deflate, br'

    def test__content_type_values(self):                                                # Test Content-Type header values
        assert Safe_Str__Http__Header__Value('application/json'                                     ) == 'application/json'
        assert Safe_Str__Http__Header__Value('text/html; charset=utf-8'                             ) == 'text/html; charset=utf-8'
        assert Safe_Str__Http__Header__Value('multipart/form-data; boundary=----WebKitFormBoundary' ) == 'multipart/form-data; boundary=----WebKitFormBoundary'
        assert Safe_Str__Http__Header__Value('application/x-www-form-urlencoded'                    ) == 'application/x-www-form-urlencoded'

    def test__authorization_values(self):                                               # Test Authorization header values
        assert Safe_Str__Http__Header__Value('Basic dXNlcjpwYXNz'                         ) == 'Basic dXNlcjpwYXNz'
        assert Safe_Str__Http__Header__Value('Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9') == 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9'
        assert Safe_Str__Http__Header__Value('Digest username="user"'                     ) == 'Digest username="user"'
        assert Safe_Str__Http__Header__Value('ApiKey abc-123-def-456'                     ) == 'ApiKey abc-123-def-456'

    def test__cache_control_values(self):                                               # Test Cache-Control header values
        assert Safe_Str__Http__Header__Value('no-cache'           ) == 'no-cache'
        assert Safe_Str__Http__Header__Value('max-age=31536000'   ) == 'max-age=31536000'
        assert Safe_Str__Http__Header__Value('private, must-revalidate') == 'private, must-revalidate'
        assert Safe_Str__Http__Header__Value('public, max-age=3600, immutable') == 'public, max-age=3600, immutable'

    def test__accept_values(self):                                                      # Test Accept header values
        assert Safe_Str__Http__Header__Value('text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8') == 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        assert Safe_Str__Http__Header__Value('application/json, text/plain, */*') == 'application/json, text/plain, */*'

    def test__user_agent_values(self):                                                  # Test User-Agent header values
        chrome = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        assert Safe_Str__Http__Header__Value(chrome            ) == chrome

        curl = 'curl/7.68.0'
        assert Safe_Str__Http__Header__Value(curl              ) == curl

    def test__special_characters_allowed(self):                                         # Test various allowed special characters
        assert Safe_Str__Http__Header__Value('value with spaces'        ) == 'value with spaces'
        assert Safe_Str__Http__Header__Value('value-with-dashes'        ) == 'value-with-dashes'
        assert Safe_Str__Http__Header__Value('value_with_underscores'   ) == 'value_with_underscores'
        assert Safe_Str__Http__Header__Value('value.with.dots'          ) == 'value.with.dots'
        assert Safe_Str__Http__Header__Value('value:with:colons'        ) == 'value:with:colons'
        assert Safe_Str__Http__Header__Value('value/with/slashes'       ) == 'value/with/slashes'
        assert Safe_Str__Http__Header__Value('value=with=equals'        ) == 'value=with=equals'
        assert Safe_Str__Http__Header__Value('value,with,commas'        ) == 'value,with,commas'
        assert Safe_Str__Http__Header__Value('value;with;semicolons'    ) == 'value;with;semicolons'
        assert Safe_Str__Http__Header__Value('"quoted-value"'           ) == '"quoted-value"'
        assert Safe_Str__Http__Header__Value('[bracketed]'              ) == '[bracketed]'
        assert Safe_Str__Http__Header__Value('{json:"value"}'           ) == '{json:"value"}'
        assert Safe_Str__Http__Header__Value('value+with+plus'          ) == 'value+with+plus'
        assert Safe_Str__Http__Header__Value('value*with*star'          ) == 'value*with*star'

    def test__whitespace_handling(self):                                                # Test trim_whitespace = True
        assert Safe_Str__Http__Header__Value('  application/json  ') == 'application/json'
        assert Safe_Str__Http__Header__Value('Bearer token  '    ) == 'Bearer token'
        assert Safe_Str__Http__Header__Value('  value  '         ) == 'value'

    def test__tab_handling(self):                                                       # Tab is allowed (0x09) but leading/trailing whitespace trimmed
        assert Safe_Str__Http__Header__Value('value\twith\ttabs') == 'value\twith\ttabs'
        assert Safe_Str__Http__Header__Value('\tvalue\t'         ) == 'value'
        assert Safe_Str__Http__Header__Value('start\tend'        ) == 'start\tend'

    def test__numeric_conversion(self):                                                 # Test conversion from numeric types
        assert Safe_Str__Http__Header__Value(12345               ) == '12345'
        assert Safe_Str__Http__Header__Value(0                   ) == '0'
        assert Safe_Str__Http__Header__Value(999999              ) == '999999'

    def test__control_characters(self):                                                 # Control characters get replaced (except tab)
        assert Safe_Str__Http__Header__Value('value\x00null'    ) == 'value_null'
        assert Safe_Str__Http__Header__Value('value\x01control' ) == 'value_control'
        assert Safe_Str__Http__Header__Value('value\x1Fescape'  ) == 'value_escape'
        assert Safe_Str__Http__Header__Value('value\x7Fdel'     ) == 'value_del'
        assert Safe_Str__Http__Header__Value('value\x0Bvtab'    ) == 'value_vtab'       # Vertical tab
        assert Safe_Str__Http__Header__Value('value\x0Cformfeed') == 'value_formfeed'   # Form feed

    def test__empty_values(self):                                                       # Test allow_empty = True
        assert Safe_Str__Http__Header__Value(None                ) == ''
        assert Safe_Str__Http__Header__Value(''                  ) == ''
        assert Safe_Str__Http__Header__Value('   '               ) == ''                # Spaces only (will be trimmed)

    def test__max_length(self):                                                         # Test TYPE_SAFE_STR__HTTP__HEADER_VALUE__MAX_LENGTH = 8192
        valid_8192   = 'a' * 8192
        invalid_8193 = 'a' * 8193

        assert Safe_Str__Http__Header__Value(valid_8192          ) == valid_8192

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__Header__Value(invalid_8193)
        assert "in Safe_Str__Http__Header__Value, value exceeds maximum length of 8192" in str(exc_info.value)

    def test__long_tokens(self):                                                        # Test long authorization tokens
        long_token = 'Bearer ' + 'a' * 2000
        assert len(Safe_Str__Http__Header__Value(long_token)     ) == len(long_token)

        long_cookie = 'session=' + 'x' * 4000 + '; user=test'
        assert len(Safe_Str__Http__Header__Value(long_cookie)    ) == len(long_cookie)

    def test__real_world_values(self):                                                  # Test real-world header values
        # Complex Accept header
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
        assert Safe_Str__Http__Header__Value(accept              ) == accept

        # AWS Signature
        aws_sig = 'AWS4-HMAC-SHA256 Credential=AKIAIOSFODNN7EXAMPLE/20130524/us-east-1/s3/aws4_request'
        assert Safe_Str__Http__Header__Value(aws_sig             ) == aws_sig

        # Cookie header
        cookie = 'session=abc123; user_id=456; preferences={"theme":"dark"}'
        assert Safe_Str__Http__Header__Value(cookie              ) == cookie

    def test__str_and_repr(self):                                                       # Test string representations
        header_value = Safe_Str__Http__Header__Value('application/json')

        assert str(header_value)      == 'application/json'
        assert f"{header_value}"      == 'application/json'
        assert f"Value: {header_value}" == 'Value: application/json'