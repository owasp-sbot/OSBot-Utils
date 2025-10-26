import pytest
from unittest                                                                     import TestCase
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Location import Safe_Str__Http__Location


class test_Safe_Str__Http__Location(TestCase):

    def test__init__(self):                                                             # Test Safe_Str__Http__Location initialization
        location = Safe_Str__Http__Location('https://example.com')
        assert type(location)         is Safe_Str__Http__Location
        assert str(location)          == 'https://example.com'
        assert location               == 'https://example.com'

    def test__absolute_urls(self):                                                      # Test absolute URL formats
        assert Safe_Str__Http__Location('https://example.com') == 'https://example.com'
        assert Safe_Str__Http__Location('https://example.com/path') == 'https://example.com/path'
        assert Safe_Str__Http__Location('https://example.com/path/to/resource') == 'https://example.com/path/to/resource'
        assert Safe_Str__Http__Location('http://example.com:8080/path') == 'http://example.com:8080/path'
        assert Safe_Str__Http__Location('https://sub.example.com/path') == 'https://sub.example.com/path'

    def test__relative_urls(self):                                                      # Test relative URL formats
        assert Safe_Str__Http__Location('/path/to/resource'  ) == '/path/to/resource'
        assert Safe_Str__Http__Location('/index.html'        ) == '/index.html'
        assert Safe_Str__Http__Location('/api/v1/users'      ) == '/api/v1/users'
        assert Safe_Str__Http__Location('/admin/dashboard'   ) == '/admin/dashboard'
        assert Safe_Str__Http__Location('/'                  ) == '/'

    def test__urls_with_query_parameters(self):                                         # Test URLs containing query strings
        assert Safe_Str__Http__Location('https://example.com?param=value') == 'https://example.com?param=value'
        assert Safe_Str__Http__Location('https://example.com?p1=v1&p2=v2') == 'https://example.com?p1=v1&p2=v2'
        assert Safe_Str__Http__Location('/search?q=test'     ) == '/search?q=test'
        assert Safe_Str__Http__Location('/path?key=value&foo=bar') == '/path?key=value&foo=bar'
        assert Safe_Str__Http__Location('/api?limit=10&offset=20') == '/api?limit=10&offset=20'

    def test__urls_with_fragments(self):                                                # Test URLs with fragment identifiers
        assert Safe_Str__Http__Location('https://example.com#top') == 'https://example.com#top'
        assert Safe_Str__Http__Location('/page#section'      ) == '/page#section'
        assert Safe_Str__Http__Location('https://example.com/docs#api-reference') == 'https://example.com/docs#api-reference'
        assert Safe_Str__Http__Location('/guide#installation') == '/guide#installation'

    def test__urls_with_ports(self):                                                    # Test URLs with explicit port numbers
        assert Safe_Str__Http__Location('https://example.com:443/path') == 'https://example.com:443/path'
        assert Safe_Str__Http__Location('http://localhost:3000/') == 'http://localhost:3000/'
        assert Safe_Str__Http__Location('http://192.168.1.1:8080/admin') == 'http://192.168.1.1:8080/admin'
        assert Safe_Str__Http__Location('http://example.com:9000/api') == 'http://example.com:9000/api'

    def test__urls_with_authentication(self):                                           # Test URLs with user authentication (rare in Location)
        assert Safe_Str__Http__Location('https://user:pass@example.com/path') == 'https://user:pass@example.com/path'
        assert Safe_Str__Http__Location('http://admin:secret@localhost:8080/') == 'http://admin:secret@localhost:8080/'

    def test__encoded_urls(self):                                                       # Test URL-encoded characters
        assert Safe_Str__Http__Location('https://example.com/path%20with%20spaces') == 'https://example.com/path%20with%20spaces'
        assert Safe_Str__Http__Location('/search?q=hello%20world') == '/search?q=hello%20world'
        assert Safe_Str__Http__Location('/path/file%2Ename.txt') == '/path/file%2Ename.txt'

    def test__international_urls(self):                                                 # Test URLs with international characters
        assert Safe_Str__Http__Location('https://münchen.de/path') == 'https://münchen.de/path'
        assert Safe_Str__Http__Location('https://例え.jp/path') == 'https://例え.jp/path'
        assert Safe_Str__Http__Location('https://example.com/path/ñoño') == 'https://example.com/path/ñoño'

    def test__common_redirect_scenarios(self):                                          # Test typical redirect patterns
        assert Safe_Str__Http__Location('/login?redirect=/dashboard') == '/login?redirect=/dashboard'
        assert Safe_Str__Http__Location('https://example.com/dashboard') == 'https://example.com/dashboard'
        assert Safe_Str__Http__Location('https://external-site.com/page') == 'https://external-site.com/page'

    def test__trailing_slash_handling(self):                                            # Test URLs with/without trailing slashes
        assert Safe_Str__Http__Location('https://example.com/path/') == 'https://example.com/path/'
        assert Safe_Str__Http__Location('/path/'             ) == '/path/'
        assert Safe_Str__Http__Location('https://example.com/') == 'https://example.com/'

    def test__complex_query_strings(self):                                              # Test complex real-world query strings
        complex = 'https://example.com/search?q=test&filter[category]=tech&sort=date&page=2&limit=20'
        assert Safe_Str__Http__Location(complex              ) == complex

        search = 'https://example.com/api?param1=value1&param2=value2&param3=value3'
        assert Safe_Str__Http__Location(search               ) == search

    def test__various_protocols(self):                                                  # Test different URL schemes
        assert Safe_Str__Http__Location('https://example.com') == 'https://example.com'
        assert Safe_Str__Http__Location('http://example.com' ) == 'http://example.com'
        assert Safe_Str__Http__Location('ftp://example.com'  ) == 'ftp://example.com'
        assert Safe_Str__Http__Location('ws://example.com'   ) == 'ws://example.com'
        assert Safe_Str__Http__Location('wss://example.com'  ) == 'wss://example.com'

    def test__whitespace_handling(self):                                                # Test trim_whitespace = True
        assert Safe_Str__Http__Location('  https://example.com  ') == 'https://example.com'
        assert Safe_Str__Http__Location('/path/to/resource  ') == '/path/to/resource'
        assert Safe_Str__Http__Location('  /index.html'      ) == '/index.html'

    def test__numeric_conversion(self):                                                 # Test conversion from numeric types
        assert Safe_Str__Http__Location(12345                ) == '12345'
        assert Safe_Str__Http__Location(999999               ) == '999999'

    def test__control_characters(self):                                                 # Control characters get replaced
        assert Safe_Str__Http__Location('https://example.com\x00/path') == 'https://example.com_/path'
        assert Safe_Str__Http__Location('/path\x01/resource' ) == '/path_/resource'
        assert Safe_Str__Http__Location('http://test\x1F.com') == 'http://test_.com'

    def test__empty_values(self):                                                       # Test allow_empty = False enforcement
        assert Safe_Str__Http__Location(None )  == ''
        assert Safe_Str__Http__Location(''   )  == ''
        assert Safe_Str__Http__Location('   ')  == ''


    def test__max_length(self):                                                         # Test TYPE_SAFE_STR__HTTP__LOCATION__MAX_LENGTH = 2048
        valid_2048   = 'https://example.com/' + 'a' * 2028                              # 'https://example.com/' = 19 chars + 2029 = 2048
        invalid_2049 = 'https://example.com/' + 'a' * 2030

        assert Safe_Str__Http__Location(valid_2048           ) == valid_2048

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__Location(invalid_2049)
        assert "in Safe_Str__Http__Location, value exceeds maximum length of 2048" in str(exc_info.value)

    def test__long_paths(self):                                                         # Test URLs with very long paths
        long_path = 'https://example.com/' + '/'.join(['segment'] * 50)
        assert Safe_Str__Http__Location(long_path            ) == long_path

    def test__subdomain_variations(self):                                               # Test various subdomain patterns
        assert Safe_Str__Http__Location('https://www.example.com') == 'https://www.example.com'
        assert Safe_Str__Http__Location('https://api.example.com') == 'https://api.example.com'
        assert Safe_Str__Http__Location('https://cdn.example.com') == 'https://cdn.example.com'
        assert Safe_Str__Http__Location('https://app.staging.example.com') == 'https://app.staging.example.com'

    def test__ip_addresses(self):                                                       # Test URLs with IP addresses instead of domains
        assert Safe_Str__Http__Location('http://192.168.1.1' ) == 'http://192.168.1.1'
        assert Safe_Str__Http__Location('http://10.0.0.1:8080') == 'http://10.0.0.1:8080'
        assert Safe_Str__Http__Location('https://127.0.0.1:3000/admin') == 'https://127.0.0.1:3000/admin'

    def test__str_and_repr(self):                                                       # Test string representations
        location = Safe_Str__Http__Location('https://example.com')

        assert str(location)          == 'https://example.com'
        assert f"{location}"          == 'https://example.com'
        assert f"Location: {location}" == 'Location: https://example.com'