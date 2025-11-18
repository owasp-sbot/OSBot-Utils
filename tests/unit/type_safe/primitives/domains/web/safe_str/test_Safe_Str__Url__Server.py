import pytest
from unittest                                                                        import TestCase
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url             import Safe_Str__Url
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Path       import Safe_Str__Url__Path
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Path_Query import Safe_Str__Url__Path_Query
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url__Server     import Safe_Str__Url__Server, TYPE_SAFE_STR__URL__SERVER__MAX_LENGTH


class test_Safe_Str__Url__Server(TestCase):

    def test_init(self):
        assert Safe_Str__Url__Server() == ''

    def test_basic_https_servers(self):
        """Test basic HTTPS server URLs"""
        assert Safe_Str__Url__Server('https://example.com'             ) == 'https://example.com'
        assert Safe_Str__Url__Server('https://api.example.com'          ) == 'https://api.example.com'
        assert Safe_Str__Url__Server('https://sub.domain.example.com'   ) == 'https://sub.domain.example.com'

    def test_basic_http_servers(self):
        """Test basic HTTP server URLs"""
        assert Safe_Str__Url__Server('http://example.org'   ) == 'http://example.org'
        assert Safe_Str__Url__Server('http://localhost'     ) == 'http://localhost'
        assert Safe_Str__Url__Server('http://api.test.com'  ) == 'http://api.test.com'

    def test_servers_with_ports(self):
        """Test server URLs with explicit port numbers"""
        assert Safe_Str__Url__Server('https://example.com:443'          ) == 'https://example.com:443'
        assert Safe_Str__Url__Server('http://localhost:8080'            ) == 'http://localhost:8080'
        assert Safe_Str__Url__Server('https://api.example.com:3000'     ) == 'https://api.example.com:3000'
        assert Safe_Str__Url__Server('http://192.168.1.1:8000'          ) == 'http://192.168.1.1:8000'

    def test_servers_with_subdomains(self):
        """Test servers with various subdomain levels"""
        assert Safe_Str__Url__Server('https://www.example.com'              ) == 'https://www.example.com'
        assert Safe_Str__Url__Server('https://api.v2.example.com'           ) == 'https://api.v2.example.com'
        assert Safe_Str__Url__Server('https://deep.sub.domain.example.com'  ) == 'https://deep.sub.domain.example.com'

    def test_servers_with_ip_addresses(self):
        """Test servers using IP addresses"""
        # IPv4
        assert Safe_Str__Url__Server('http://192.168.1.1'       ) == 'http://192.168.1.1'
        assert Safe_Str__Url__Server('https://10.0.0.1'         ) == 'https://10.0.0.1'
        assert Safe_Str__Url__Server('http://127.0.0.1:8080'    ) == 'http://127.0.0.1:8080'
        assert Safe_Str__Url__Server('https://8.8.8.8:443'      ) == 'https://8.8.8.8:443'

    def test_servers_with_numeric_domains(self):
        """Test servers with numbers in domain names"""
        assert Safe_Str__Url__Server('https://api2.example.com'         ) == 'https://api2.example.com'
        assert Safe_Str__Url__Server('https://server123.example.com'    ) == 'https://server123.example.com'
        assert Safe_Str__Url__Server('https://v2.api.example.com'       ) == 'https://v2.api.example.com'

    def test_whitespace_handling(self):
        """Test trimming of leading/trailing whitespace"""
        assert Safe_Str__Url__Server('  https://example.com  '  ) == 'https://example.com'
        assert Safe_Str__Url__Server('\thttps://example.com\n'  ) == 'https://example.com'
        assert Safe_Str__Url__Server('  http://localhost:8080 ') == 'http://localhost:8080'

    def test_empty_values(self):
        """Test that empty and None values are handled correctly"""
        assert Safe_Str__Url__Server(None) == ''
        assert Safe_Str__Url__Server(''  ) == ''

    def test_invalid_missing_scheme(self):
        """Test that URLs without scheme are rejected"""
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('example.com')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('www.example.com')
        assert "does not match required pattern" in str(exc_info.value)

    def test_invalid_wrong_scheme(self):
        """Test that only http/https schemes are accepted"""
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('ftp://example.com')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('ws://example.com')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('file:///path')
        assert "does not match required pattern" in str(exc_info.value)

    def test_invalid_with_path(self):
        """Test that paths are not allowed in server component"""
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('https://example.com/path')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('https://example.com/api/v1')
        assert "does not match required pattern" in str(exc_info.value)

    def test_invalid_with_query(self):
        """Test that query parameters are not allowed"""
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('https://example.com?query=test')
        assert "does not match required pattern" in str(exc_info.value)

    def test_invalid_port_numbers(self):
        """Test that invalid port numbers are rejected"""
        # Port too high
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('https://example.com:99999')
        assert "Invalid port in server URL" in str(exc_info.value)

        # Port 0 (invalid)
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('https://example.com:0')
        assert "Invalid port" in str(exc_info.value)

        # Negative port
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('https://example.com:-1')
        assert "does not match required pattern" in str(exc_info.value)

    def test_max_length_validation(self):
        """Test max length enforcement"""
        # Within limit
        long_subdomain = 'sub' + 'a' * 50 + '.example.com'
        assert len(Safe_Str__Url__Server(f'https://{long_subdomain}')) > 0

        # Exceeds limit
        with pytest.raises(ValueError) as exc_info:
            very_long_domain = 'sub' + 'a' * 300 + '.example.com'
            Safe_Str__Url__Server(f'https://{very_long_domain}')
        assert f"exceeds maximum length of {TYPE_SAFE_STR__URL__SERVER__MAX_LENGTH}" in str(exc_info.value)

    def test_server_concatenation__server_plus_path(self):
        """Test Server + Path = Url"""
        server = Safe_Str__Url__Server('https://api.example.com')
        path = Safe_Str__Url__Path('/users/123')
        
        result = server + path
        assert type(result) is Safe_Str__Url
        assert str(result) == 'https://api.example.com/users/123'

        # Server with trailing slash
        server2 = Safe_Str__Url__Server('https://example.com')
        path2 = Safe_Str__Url__Path('/api/v1/users')
        result2 = server2 + path2
        assert str(result2) == 'https://example.com/api/v1/users'

        # Path without leading slash
        path3 = Safe_Str__Url__Path('api/users')
        result3 = server + path3
        assert str(result3) == 'https://api.example.com/api/users'

    def test_server_concatenation__server_plus_path_query(self):
        """Test Server + Path_Query = Url"""
        server = Safe_Str__Url__Server('https://api.example.com')
        path_query = Safe_Str__Url__Path_Query('/users?page=1&limit=10')
        
        result = server + path_query
        assert type(result) is Safe_Str__Url
        assert str(result) == 'https://api.example.com/users?page=1&limit=10'

        # Path_Query without leading slash
        path_query2 = Safe_Str__Url__Path_Query('search?q=test')
        result2 = server + path_query2
        assert str(result2) == 'https://api.example.com/search?q=test'

    def test_server_concatenation__server_plus_raw_path_string(self):
        """Test Server + raw path string = Url"""
        server = Safe_Str__Url__Server('https://example.com')
        
        result = server + '/api/users'
        assert type(result) is Safe_Str__Url
        assert str(result) == 'https://example.com/api/users'

        result2 = server + '/search?q=test'
        assert str(result2) == 'https://example.com/search?q=test'

    def test_server_concatenation__with_ports(self):
        """Test Server concatenation when port is present"""
        server = Safe_Str__Url__Server('http://localhost:8080')
        path = Safe_Str__Url__Path('/api/v1/users')
        
        result = server + path
        assert str(result) == 'http://localhost:8080/api/v1/users'

        path_query = Safe_Str__Url__Path_Query('/search?q=test')
        result2 = server + path_query
        assert str(result2) == 'http://localhost:8080/search?q=test'

    def test_localhost_variations(self):
        """Test localhost and loopback addresses"""
        assert Safe_Str__Url__Server('http://localhost'         ) == 'http://localhost'
        assert Safe_Str__Url__Server('https://localhost:443'    ) == 'https://localhost:443'
        assert Safe_Str__Url__Server('http://127.0.0.1'         ) == 'http://127.0.0.1'
        assert Safe_Str__Url__Server('http://127.0.0.1:3000'    ) == 'http://127.0.0.1:3000'

    def test_common_server_patterns(self):
        """Test common server URL patterns"""
        # API servers
        assert Safe_Str__Url__Server('https://api.github.com'       ) == 'https://api.github.com'
        assert Safe_Str__Url__Server('https://api.stripe.com'       ) == 'https://api.stripe.com'
        assert Safe_Str__Url__Server('https://graph.facebook.com'   ) == 'https://graph.facebook.com'

        # Development servers
        assert Safe_Str__Url__Server('http://localhost:3000'        ) == 'http://localhost:3000'
        assert Safe_Str__Url__Server('http://localhost:8000'        ) == 'http://localhost:8000'
        assert Safe_Str__Url__Server('http://dev.example.com'       ) == 'http://dev.example.com'

        # Staging servers
        assert Safe_Str__Url__Server('https://staging.example.com'  ) == 'https://staging.example.com'
        assert Safe_Str__Url__Server('https://staging-api.example.com') == 'https://staging-api.example.com'

    def test_string_representation(self):
        """Test string conversion methods"""
        server = Safe_Str__Url__Server('https://api.example.com:8080')
        
        assert str(server)  == 'https://api.example.com:8080'
        assert repr(server) == "Safe_Str__Url__Server('https://api.example.com:8080')"
        assert f"Server: {server}" == "Server: https://api.example.com:8080"

    def test_equality_and_comparison(self):
        """Test server equality"""
        server1 = Safe_Str__Url__Server('https://api.example.com')
        server2 = Safe_Str__Url__Server('https://api.example.com')
        server3 = Safe_Str__Url__Server('https://api.other.com')

        assert server1 == server2
        assert server1 == 'https://api.example.com'
        assert server1 != server3

    def test_immutability(self):
        """Test that servers are immutable"""
        server1 = Safe_Str__Url__Server('https://example.com')
        server2 = Safe_Str__Url__Server('https://example.com')

        assert server1 == server2
        assert server1 is not server2
        assert hash(server1) == hash(server2)

    def test_edge_cases(self):
        """Test various edge cases"""
        # Single character domain components
        assert Safe_Str__Url__Server('https://a.b.c') == 'https://a.b.c'

        # Maximum length domain label (63 chars)
        max_label = 'a' * 63
        assert Safe_Str__Url__Server(f'https://{max_label}.example.com') == \
               f'https://{max_label}.example.com'

        # Minimum port (1)
        assert Safe_Str__Url__Server('https://example.com:1') == 'https://example.com:1'

        # Maximum valid port (65535)
        assert Safe_Str__Url__Server('https://example.com:65535') == 'https://example.com:65535'

        # Common ports
        assert Safe_Str__Url__Server('http://example.com:80'    ) == 'http://example.com:80'
        assert Safe_Str__Url__Server('https://example.com:443'  ) == 'https://example.com:443'

    def test_domain_validation(self):
        """Test domain name validation"""
        # Valid domains
        assert Safe_Str__Url__Server('https://example.com'      ) == 'https://example.com'
        assert Safe_Str__Url__Server('https://my-site.com'      ) == 'https://my-site.com'
        assert Safe_Str__Url__Server('https://site123.com'      ) == 'https://site123.com'

        # Invalid: starts with hyphen
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('https://-example.com')
        assert "Invalid host" in str(exc_info.value)

        # Invalid: ends with hyphen
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('https://example-.com')
        assert "Invalid host" in str(exc_info.value)

    def test__ip_validation(self):
        """Test IP address validation"""
        # Valid IPv4
        assert Safe_Str__Url__Server('http://0.0.0.0'       ) == 'http://0.0.0.0'
        assert Safe_Str__Url__Server('http://255.255.255.255') == 'http://255.255.255.255'

        # Invalid IPv4
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('http://256.1.1.1')
        assert "Invalid host" in str(exc_info.value)


        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('http://1.1.1.999')
        assert "Invalid host" in str(exc_info.value)

    def test_ip_validation(self):
        """Test IP address validation"""
        # Valid IPv4
        assert Safe_Str__Url__Server('http://0.0.0.0'          ) == 'http://0.0.0.0'
        assert Safe_Str__Url__Server('http://255.255.255.255'  ) == 'http://255.255.255.255'
        assert Safe_Str__Url__Server('http://192.168.1.1'      ) == 'http://192.168.1.1'
        assert Safe_Str__Url__Server('http://10.0.0.1'         ) == 'http://10.0.0.1'
        assert Safe_Str__Url__Server('http://127.0.0.1'        ) == 'http://127.0.0.1'

        # Invalid IPv4 - octets > 255
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('http://256.1.1.1')
        assert "appears to be an invalid IP address" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('http://1.1.1.999')
        assert "appears to be an invalid IP address" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('http://300.200.100.50')
        assert "appears to be an invalid IP address" in str(exc_info.value)

        # Invalid IPv4 - wrong format
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('http://1.1.1')  # Only 3 octets
        assert "Invalid host" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('http://1.1.1.1.1')  # 5 octets
        assert "Invalid host" in str(exc_info.value)

        # Edge cases
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('http://01.1.1.1')  # Leading zero
        assert "appears to be an invalid IP address" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('http://1.1.1.-1')  # Negative
        assert "Invalid host" in str(exc_info.value)  # Not all digits

    def test_numeric_domains_vs_ips(self):
        """Test that we correctly distinguish numeric domains from invalid IPs"""
        # Valid: domains with numbers (but not all numeric)
        assert Safe_Str__Url__Server('https://api2.example.com'    ) == 'https://api2.example.com'
        assert Safe_Str__Url__Server('https://123.example.com'     ) == 'https://123.example.com'
        assert Safe_Str__Url__Server('https://server1.server2.com' ) == 'https://server1.server2.com'

        # Invalid: all-numeric but not 4 parts (domain validation fails)
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('https://123.456')
        assert "Invalid host" in str(exc_info.value)

        # Invalid: looks like IP but has invalid octets
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url__Server('https://256.256.256.256')
        assert "appears to be an invalid IP address" in str(exc_info.value)

        # Valid: numeric TLD is technically allowed in domains
        assert Safe_Str__Url__Server('https://example.123') == 'https://example.123'