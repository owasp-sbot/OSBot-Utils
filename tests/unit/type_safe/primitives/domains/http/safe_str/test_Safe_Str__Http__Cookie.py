import pytest
from unittest                                                                   import TestCase
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Cookie import Safe_Str__Http__Cookie, TYPE_SAFE_STR__HTTP__COOKIE__MAX_LENGTH


class test_Safe_Str__Http__Cookie(TestCase):

    def test__init__(self):                                                             # Test Safe_Str__Http__Cookie initialization
        cookie = Safe_Str__Http__Cookie('session=abc123')
        assert type(cookie)           is Safe_Str__Http__Cookie
        assert str(cookie)            == 'session=abc123'
        assert cookie                 == 'session=abc123'

    def test__simple_cookies(self):                                                     # Test simple cookie name=value pairs
        assert Safe_Str__Http__Cookie('session=abc123'       ) == 'session=abc123'
        assert Safe_Str__Http__Cookie('user_id=456'          ) == 'user_id=456'
        assert Safe_Str__Http__Cookie('theme=dark'           ) == 'theme=dark'
        assert Safe_Str__Http__Cookie('language=en'          ) == 'language=en'
        assert Safe_Str__Http__Cookie('token=xyz789'         ) == 'token=xyz789'

    def test__multiple_cookies(self):                                                   # Test multiple cookies in one header
        assert Safe_Str__Http__Cookie('session=abc123; user_id=456') == 'session=abc123; user_id=456'
        assert Safe_Str__Http__Cookie('session=abc123; user_id=456; theme=dark') == 'session=abc123; user_id=456; theme=dark'
        assert Safe_Str__Http__Cookie('a=1; b=2; c=3; d=4'   ) == 'a=1; b=2; c=3; d=4'

    def test__cookies_with_special_characters(self):                                    # Test cookies containing various characters
        assert Safe_Str__Http__Cookie('token=abc-def-123'    ) == 'token=abc-def-123'
        assert Safe_Str__Http__Cookie('data=value_with_underscores') == 'data=value_with_underscores'
        assert Safe_Str__Http__Cookie('url=https://example.com/path') == 'url=https://example.com/path'
        assert Safe_Str__Http__Cookie('path=/admin/dashboard') == 'path=/admin/dashboard'

    def test__cookies_with_encoded_values(self):                                        # Test URL-encoded cookie values
        assert Safe_Str__Http__Cookie('data=eyJuYW1lIjoiSm9obiJ9') == 'data=eyJuYW1lIjoiSm9obiJ9'
        assert Safe_Str__Http__Cookie('preferences=%7B%22theme%22%3A%22dark%22%7D') == 'preferences=%7B%22theme%22%3A%22dark%22%7D'
        assert Safe_Str__Http__Cookie('name=John+Doe'        ) == 'name=John+Doe'
        assert Safe_Str__Http__Cookie('name=John%20Doe'      ) == 'name=John%20Doe'

    def test__cookies_with_json_like_values(self):                                      # Test cookies with JSON-style values
        assert Safe_Str__Http__Cookie('settings={"theme":"dark","lang":"en"}') == 'settings={"theme":"dark","lang":"en"}'
        assert Safe_Str__Http__Cookie('preferences={"notifications":true}') == 'preferences={"notifications":true}'

    def test__session_cookies(self):                                                    # Test session-related cookies
        assert Safe_Str__Http__Cookie('PHPSESSID=abcdef1234567890; path=/; HttpOnly') == 'PHPSESSID=abcdef1234567890; path=/; HttpOnly'
        assert Safe_Str__Http__Cookie('JSESSIONID=9F1E2D3C4B5A6978') == 'JSESSIONID=9F1E2D3C4B5A6978'
        assert Safe_Str__Http__Cookie('sessionId=a1b2c3d4e5f6g7h8') == 'sessionId=a1b2c3d4e5f6g7h8'

    def test__jwt_cookies(self):                                                        # Test JWT token cookies
        jwt = 'auth_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abc123'
        assert Safe_Str__Http__Cookie(jwt                    ) == jwt

    def test__analytics_cookies(self):                                                  # Test analytics service cookies
        ga = '_ga=GA1.2.123456789.1234567890; _gid=GA1.2.987654321.1234567890'
        assert Safe_Str__Http__Cookie(ga                     ) == ga

        gtm = '_ga=GA1.2.1234567890; _gat=1; _gid=GA1.2.9876543210'
        assert Safe_Str__Http__Cookie(gtm                    ) == gtm

    def test__cookies_with_equals_in_value(self):                                       # Test cookies where value contains equals sign
        assert Safe_Str__Http__Cookie('data=key=value'       ) == 'data=key=value'
        assert Safe_Str__Http__Cookie('query=param1=val1&param2=val2') == 'query=param1=val1&param2=val2'

    def test__cookies_with_quotes(self):                                                # Test cookies with quoted values
        assert Safe_Str__Http__Cookie('name="John Doe"'      ) == 'name="John Doe"'
        assert Safe_Str__Http__Cookie('message="Hello, World!"') == 'message="Hello, World!"'

    def test__whitespace_handling(self):                                                # Test trim_whitespace = True
        assert Safe_Str__Http__Cookie('  session=abc123  '   ) == 'session=abc123'
        assert Safe_Str__Http__Cookie('session=abc123; user_id=456  ') == 'session=abc123; user_id=456'
        assert Safe_Str__Http__Cookie('  token=xyz'          ) == 'token=xyz'

    def test__numeric_conversion(self):                                                 # Test conversion from numeric types
        assert Safe_Str__Http__Cookie(12345                  ) == '12345'
        assert Safe_Str__Http__Cookie(999999                 ) == '999999'

    def test__control_characters(self):                                                 # Control characters get replaced
        assert Safe_Str__Http__Cookie('session=abc\x00123'   ) == 'session=abc_123'
        assert Safe_Str__Http__Cookie('user\x01id=456'       ) == 'user_id=456'
        assert Safe_Str__Http__Cookie('token\x1F=xyz'        ) == 'token_=xyz'

    def test__empty_values(self):                                                       # Test allow_empty = True
        assert Safe_Str__Http__Cookie(None                   ) == ''
        assert Safe_Str__Http__Cookie(''                     ) == ''
        assert Safe_Str__Http__Cookie('   '                  ) == ''                    # Spaces only (will be trimmed)

    def test__max_length(self):                                                         # Test TYPE_SAFE_STR__HTTP__COOKIE__MAX_LENGTH = 4096
        valid_32768   = 'a' * 32768
        invalid_32769 = 'a' * 32769

        assert Safe_Str__Http__Cookie(valid_32768             ) == valid_32768

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__Cookie(invalid_32769)
        assert f"in Safe_Str__Http__Cookie, value exceeds maximum length of {TYPE_SAFE_STR__HTTP__COOKIE__MAX_LENGTH}" in str(exc_info.value)

    def test__long_cookie_strings(self):                                                # Test long cookie value strings
        long_session = 'session=' + 'a' * 2000
        assert len(Safe_Str__Http__Cookie(long_session)      ) == len(long_session)

        long_multi = 'token1=' + 'x' * 1000 + '; token2=' + 'y' * 1000 + '; token3=' + 'z' * 1000
        assert len(Safe_Str__Http__Cookie(long_multi)        ) == len(long_multi)

    def test__real_world_cookies(self):                                                 # Test real-world cookie patterns
        # Authentication cookies
        auth = 'access_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9; refresh_token=def50200abc'
        assert Safe_Str__Http__Cookie(auth                   ) == auth

        # E-commerce cookies
        ecommerce = 'cart_id=12345; user_id=67890; session_start=1609459200'
        assert Safe_Str__Http__Cookie(ecommerce              ) == ecommerce

        # Tracking cookies
        tracking = 'utm_source=google; utm_medium=cpc; utm_campaign=spring_sale'
        assert Safe_Str__Http__Cookie(tracking               ) == tracking

    def test__cookie_attributes(self):                                                  # Test cookies with attribute flags
        assert Safe_Str__Http__Cookie('session=abc; Secure'  ) == 'session=abc; Secure'
        assert Safe_Str__Http__Cookie('session=abc; HttpOnly') == 'session=abc; HttpOnly'
        assert Safe_Str__Http__Cookie('session=abc; SameSite=Strict') == 'session=abc; SameSite=Strict'
        assert Safe_Str__Http__Cookie('session=abc; Secure; HttpOnly; SameSite=Lax') == 'session=abc; Secure; HttpOnly; SameSite=Lax'

    def test__str_and_repr(self):                                                       # Test string representations
        cookie = Safe_Str__Http__Cookie('session=abc123')

        assert str(cookie)            == 'session=abc123'
        assert f"{cookie}"            == 'session=abc123'
        assert f"Cookie: {cookie}"    == 'Cookie: session=abc123'