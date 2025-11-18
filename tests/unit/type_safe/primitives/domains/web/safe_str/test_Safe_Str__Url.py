import re

import pytest
from unittest                                                                import TestCase
from osbot_utils.type_safe.primitives.domains.web.safe_str.Safe_Str__Url     import Safe_Str__Url, TYPE_SAFE_STR__URL__MAX_LENGTH


class test_Safe_Str__Url(TestCase):

    def test_init(self):
        assert Safe_Str__Url() == ''

    def test_basic_urls(self):
        """Test basic URL validation with various schemes and domains"""
        assert Safe_Str__Url('https://example.com'              ) == 'https://example.com'
        assert Safe_Str__Url('http://example.org'               ) == 'http://example.org'
        assert Safe_Str__Url('https://sub.domain.example.com'   ) == 'https://sub.domain.example.com'

    def test_urls_with_paths(self):
        """Test URLs with path components"""
        assert Safe_Str__Url('https://example.com/path/to/resource'     ) == 'https://example.com/path/to/resource'
        assert Safe_Str__Url('https://example.com/path/to/resource.html') == 'https://example.com/path/to/resource.html'
        assert Safe_Str__Url('https://example.com/api/v1/users'         ) == 'https://example.com/api/v1/users'

    def test_urls_with_query_parameters(self):
        """Test URLs with query strings"""
        assert Safe_Str__Url('https://example.com/search?q=test'                   ) == 'https://example.com/search?q=test'
        assert Safe_Str__Url('https://example.com/path?param1=value1&param2=value2') == 'https://example.com/path?param1=value1&param2=value2'
        assert Safe_Str__Url('https://example.com/path?q=hello+world'              ) == 'https://example.com/path?q=hello+world'
        assert Safe_Str__Url('https://example.com/path?q=test%20value'             ) == 'https://example.com/path?q=test%20value'

    def test_urls_with_fragments(self):
        """Test URLs with fragment identifiers"""
        assert Safe_Str__Url('https://example.com/page#section1'       ) == 'https://example.com/page#section1'
        assert Safe_Str__Url('https://example.com/docs#top'            ) == 'https://example.com/docs#top'
        assert Safe_Str__Url('https://example.com/page?q=test#section') == 'https://example.com/page?q=test#section'

    def test_urls_with_ports(self):
        """Test URLs with explicit port numbers"""
        assert Safe_Str__Url('http://localhost:8080'           ) == 'http://localhost:8080'
        assert Safe_Str__Url('https://example.com:443/secure'  ) == 'https://example.com:443/secure'
        assert Safe_Str__Url('http://192.168.1.1:3000/api'     ) == 'http://192.168.1.1:3000/api'

    def test_urls_with_authentication__not_allowed(self):
        """Test URLs with user credentials"""
        error_message = "in Safe_Str__Url, value does not match required pattern: ^https?://[a-zA-Z0-9.\\-]+(:[0-9]{1,5})?(/[a-zA-Z0-9/\\-._~%]*)?(\\?[a-zA-Z0-9=&\\-._~%+]*)?(#[a-zA-Z0-9\\-._~%]*)?$"
        with pytest.raises(ValueError, match=re.escape(error_message)):
            Safe_Str__Url('https://user:pass@example.com'     )
        # assert Safe_Str__Url('https://user:pass@example.com'     ) == 'https://user:pass@example.com'
        # assert Safe_Str__Url('https://user@example.com'          ) == 'https://user@example.com'
        # assert Safe_Str__Url('https://user:pass@example.com:8080') == 'https://user:pass@example.com:8080'

    def test_url_encoding(self):
        """Test URLs with percent-encoded characters"""
        assert Safe_Str__Url('https://example.com/search?q=hello%20world'  ) == 'https://example.com/search?q=hello%20world'
        assert Safe_Str__Url('https://example.com/path%20with%20spaces'    ) == 'https://example.com/path%20with%20spaces'
        assert Safe_Str__Url('https://example.com/search?q=%22quoted%22'   ) == 'https://example.com/search?q=%22quoted%22'
        assert Safe_Str__Url('https://example.com/%7Euser/profile'         ) == 'https://example.com/%7Euser/profile'
        assert Safe_Str__Url('https://example.com/caf%C3%A9'               ) == 'https://example.com/caf%C3%A9'

    def test_whitespace_handling(self):
        """Test trimming of leading/trailing whitespace"""
        assert Safe_Str__Url('  https://example.com  ') == 'https://example.com'
        assert Safe_Str__Url('\thttps://example.com\n') == 'https://example.com'
        assert Safe_Str__Url('\n  https://example.com  \t') == 'https://example.com'

    def test_empty_values(self):
        """Test that empty and None values are handled correctly"""
        assert Safe_Str__Url(None) == ''
        assert Safe_Str__Url(''  ) == ''

    def test_max_length_validation(self):
        """Test that URLs exceeding max length are rejected"""
        valid_url = 'https://example.com/' + 'a' * (TYPE_SAFE_STR__URL__MAX_LENGTH - 50)
        assert len(Safe_Str__Url(valid_url)) > 0

        with pytest.raises(ValueError) as exc_info:
            invalid_url = 'https://example.com/' + 'a' * TYPE_SAFE_STR__URL__MAX_LENGTH
            Safe_Str__Url(invalid_url)
        assert f"exceeds maximum length of {TYPE_SAFE_STR__URL__MAX_LENGTH}" in str(exc_info.value)

    def test_invalid_schemes(self):
        """Test that only http/https schemes are accepted"""
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url('ftp://example.com')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url('ws://example.com')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url('file:///path/to/file')
        assert "does not match required pattern" in str(exc_info.value)

    def test_missing_scheme(self):
        """Test that URLs without scheme are rejected"""
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url('example.com')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url('www.example.com')
        assert "does not match required pattern" in str(exc_info.value)

    def test_string_representation(self):
        """Test string conversion methods"""
        url = Safe_Str__Url('https://example.com/path?query=test&foo=bar')

        assert str(url)  == 'https://example.com/path?query=test&foo=bar'
        assert repr(url) == "Safe_Str__Url('https://example.com/path?query=test&foo=bar')"
        assert f"Visit: {url}" == "Visit: https://example.com/path?query=test&foo=bar"

    def test_equality_and_comparison(self):
        """Test URL equality and comparison"""
        url1 = Safe_Str__Url('https://example.com/path')
        url2 = Safe_Str__Url('https://example.com/path')
        url3 = Safe_Str__Url('https://example.com/other')

        assert url1 == url2
        assert url1 == 'https://example.com/path'
        assert url1 != url3

    def test_immutability(self):
        """Test that URLs are immutable string-like objects"""
        url1 = Safe_Str__Url('https://example.com')
        url2 = Safe_Str__Url('https://example.com')

        assert url1 == url2
        assert url1 is not url2
        assert hash(url1) == hash(url2)

    def test_api_patterns(self):
        """Test common API URL patterns"""
        assert Safe_Str__Url('https://api.example.com/v1/users'             ) == 'https://api.example.com/v1/users'
        assert Safe_Str__Url('https://api.example.com/v2/users/123'         ) == 'https://api.example.com/v2/users/123'
        assert Safe_Str__Url('https://api.example.com/graphql'              ) == 'https://api.example.com/graphql'
        assert Safe_Str__Url('https://api.example.com/webhooks/github'      ) == 'https://api.example.com/webhooks/github'

    def test_localhost_patterns(self):
        """Test localhost and development URLs"""
        assert Safe_Str__Url('http://localhost:3000'            ) == 'http://localhost:3000'
        assert Safe_Str__Url('http://localhost:8080/api'        ) == 'http://localhost:8080/api'
        assert Safe_Str__Url('http://127.0.0.1:8000'            ) == 'http://127.0.0.1:8000'
        assert Safe_Str__Url('http://192.168.1.100:5000/admin'  ) == 'http://192.168.1.100:5000/admin'

    def test_complex_urls(self):
        """Test complex real-world URL patterns"""
        assert Safe_Str__Url('https://api.github.com/repos/owner/repo/issues?state=open&sort=created') == \
               'https://api.github.com/repos/owner/repo/issues?state=open&sort=created'

        assert Safe_Str__Url('https://example.com/search?q=python+tutorial&category=programming&page=1') == \
               'https://example.com/search?q=python+tutorial&category=programming&page=1'

    def test_edge_cases(self):
        """Test various edge cases"""
        # Minimal valid URL
        assert Safe_Str__Url('https://a.b') == 'https://a.b'

        # URL with only scheme and domain
        assert Safe_Str__Url('https://example.com') == 'https://example.com'

        # URL with trailing slash
        assert Safe_Str__Url('https://example.com/') == 'https://example.com/'

        # URL with multiple slashes in path
        assert Safe_Str__Url('https://example.com/path//to///resource') == 'https://example.com/path//to///resource'