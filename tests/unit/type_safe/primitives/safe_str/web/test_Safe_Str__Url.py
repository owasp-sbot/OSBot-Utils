import pytest
from unittest                                                    import TestCase
from osbot_utils.type_safe.primitives.safe_str.Safe_Str          import Safe_Str
from osbot_utils.type_safe.primitives.safe_str.web.Safe_Str__Url import Safe_Str__Url, TYPE_SAFE_STR__URL__MAX_LENGTH


class test_Safe_Str__Url(TestCase):

    def test_Safe_Str__Url_class(self):
        # Valid URLs
        assert Safe_Str__Url('https://example.com'                                       ) == 'https://example.com'
        assert Safe_Str__Url('http://example.org'                                        ) == 'http://example.org'
        assert Safe_Str__Url('https://sub.domain.example.com'                            ) == 'https://sub.domain.example.com'
        assert Safe_Str__Url('https://example.com/path/to/resource'                      ) == 'https://example.com/path/to/resource'
        assert Safe_Str__Url('https://example.com/path/to/resource.html'                 ) == 'https://example.com/path/to/resource.html'
        
        # URLs with query parameters
        assert str(Safe_Str__Url('https://example.com/search?q=test'                    )) == 'https://example.com/search?q=test'                       # todo: remove the str(...) from these tests since they are not needed, since Safe_Str__Url(Safe_Str(str))
        assert str(Safe_Str__Url('https://example.com/path?param1=value1&param2=value2' )) == 'https://example.com/path?param1=value1&param2=value2'
        assert str(Safe_Str__Url('https://example.com/path?q=hello+world'               )) == 'https://example.com/path?q=hello+world'
        assert str(Safe_Str__Url('https://example.com/path?q=test%20value'              )) == 'https://example.com/path?q=test%20value'
        
        # URLs with fragments
        assert str(Safe_Str__Url('https://example.com/page#section1'                    )) == 'https://example.com/page#section1'
        assert str(Safe_Str__Url('https://example.com/docs#top'                         )) == 'https://example.com/docs#top'

        # URLs with port numbers
        assert str(Safe_Str__Url('http://localhost:8080'                                )) == 'http://localhost:8080'
        assert str(Safe_Str__Url('https://example.com:443/secure'                       )) == 'https://example.com:443/secure'
        
        # URLs with authentication
        assert str(Safe_Str__Url('https://user:pass@example.com'                        )) == 'https://user:pass@example.com'
        
        # Spaces and trimming (should be trimmed and replaced)
        assert str(Safe_Str__Url('  https://example.com  '                              )) == 'https://example.com'
        assert str(Safe_Str__Url('https://example.com/path with spaces'                 )) == 'https://example.com/path_with_spaces'
        
        # Invalid characters get replaced
        assert str(Safe_Str__Url('https://example.com/<script>'                         )) == 'https://example.com/_script_'
        assert str(Safe_Str__Url('https://example.com/"quote"'                          )) == 'https://example.com/_quote_'
        assert str(Safe_Str__Url('https://example.com/test|pipe'                        )) == 'https://example.com/test_pipe'
        assert str(Safe_Str__Url('https://user@example.com'                             )) == 'https://user@example.com'                    # todo: see security implications of allow this
        
        # Security-sensitive examples
        assert Safe_Str__Url('https://example.com/../../etc/passwd'                 ) == 'https://example.com/../../etc/passwd'             # we can't do much about this here since this is a valid url
        assert Safe_Str__Url('https://evil.com/<script>alert(1)</script>'           ) == 'https://evil.com/_script_alert_1__/script_'       # this one we can remove the < >
        assert Safe_Str__Url('https://<><><><>')                                     == 'https://________'                                  # todo: see if this should raise

        # Query parameters with special characters
        assert str(Safe_Str__Url('https://example.com/search?q=test&lang=en'            )) == 'https://example.com/search?q=test&lang=en'
        assert str(Safe_Str__Url('https://example.com/path?param=value+with+spaces'     )) == 'https://example.com/path?param=value+with+spaces'
        assert str(Safe_Str__Url('https://example.com/search?q=test&param="invalid"'    )) == 'https://example.com/search?q=test&param=_invalid_'

        # Empty values allowed
        assert Safe_Str__Url(None) == ''
        assert Safe_Str__Url(''  ) == ''

        # Edge cases: exceptions with specific error message checks
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url('example.com')  # Missing scheme
        assert "in Safe_Str__Url, sanitized value consists entirely of '_' characters" in str(exc_info.value)                             # todo : find better way to handle this scenario (this error comes from Safe_Str
        
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Url('ftp://example.com')  # Invalid scheme (only http/https allowed)
        assert "in Safe_Str__Url, sanitized value consists entirely of '_' characters" in str(exc_info.value)                             # todo : find better way to handle this scenario (this error comes from Safe_Str
        
        with pytest.raises(ValueError) as exc_info:  # exceeds max length
            Safe_Str__Url('https://example.com/' + 'a' * TYPE_SAFE_STR__URL__MAX_LENGTH)
        assert f"in Safe_Str__Url, value exceeds maximum length of {TYPE_SAFE_STR__URL__MAX_LENGTH}" in str(exc_info.value)


    def test_url_components(self):                                                                                      # Tests specific to URL components.
        # Different schemes
        assert str(Safe_Str__Url('https://example.com'                      )) == 'https://example.com'
        assert str(Safe_Str__Url('http://example.com'                       )) == 'http://example.com'
        
        # Subdomains
        assert str(Safe_Str__Url('https://sub.example.com'                  )) == 'https://sub.example.com'
        assert str(Safe_Str__Url('https://sub.sub.example.com'              )) == 'https://sub.sub.example.com'
        
        # Path components
        assert str(Safe_Str__Url('https://example.com/path'                 )) == 'https://example.com/path'
        assert str(Safe_Str__Url('https://example.com/path/to/resource'     )) == 'https://example.com/path/to/resource'
        assert str(Safe_Str__Url('https://example.com/path/to/resource.html')) == 'https://example.com/path/to/resource.html'
        
        # Query string
        assert str(Safe_Str__Url('https://example.com/search?q=test'                    )) == 'https://example.com/search?q=test'
        assert str(Safe_Str__Url('https://example.com/path?param1=value1&param2=value2' )) == 'https://example.com/path?param1=value1&param2=value2'
        
        # Fragment/anchor
        assert str(Safe_Str__Url('https://example.com/page#section'         )) == 'https://example.com/page#section'
        assert str(Safe_Str__Url('https://example.com/page?q=test#section'  )) == 'https://example.com/page?q=test#section'
        
    def test_url_encoding(self):                                                                                        # Tests for URL encoding.
        # URL-encoded characters
        assert str(Safe_Str__Url('https://example.com/search?q=hello%20world'   )) == 'https://example.com/search?q=hello%20world'
        assert str(Safe_Str__Url('https://example.com/path%20with%20spaces'     )) == 'https://example.com/path%20with%20spaces'
        assert str(Safe_Str__Url('https://example.com/search?q=%22quoted%22'    )) == 'https://example.com/search?q=%22quoted%22'
        
        # Plus sign as space in query parameters
        assert str(Safe_Str__Url('https://example.com/search?q=hello+world'     )) == 'https://example.com/search?q=hello+world'
        
        # Special characters in URL paths
        assert str(Safe_Str__Url('https://example.com/%7Euser/profile'          )) == 'https://example.com/%7Euser/profile'
        assert str(Safe_Str__Url('https://example.com/caf%C3%A9'                )) == 'https://example.com/caf%C3%A9'

    def test_edge_cases(self):
        assert Safe_Str__Url() == ''

    def test__safe_str__concat_with_validation(self):
        # Test that validation/sanitization still applies after concatenation
        url = Safe_Str__Url('https://example.com/path')
        result = url + '?query="test"'  # Should sanitize the quotes

        assert type(result) is Safe_Str__Url
        assert '"' not in str(result)  # Quotes should be sanitized

        # Test max length enforcement
        short_str = Safe_Str('a' * 500)  # Near max length
        with pytest.raises(ValueError, match="exceeds maximum length"):
            short_str + ('b' * 20)  # Should exceed max length

    def test__safe_str_url__string_representation(self):
        # URL with query params
        url = Safe_Str__Url('https://example.com/path?query=test&foo=bar')
        assert str(url) == 'https://example.com/path?query=test&foo=bar'
        assert f"Visit: {url}" == "Visit: https://example.com/path?query=test&foo=bar"
        assert repr(url) == "Safe_Str__Url('https://example.com/path?query=test&foo=bar')"

        # URL with sanitization
        url_sanitized = Safe_Str__Url('https://example.com/path?q="test"')
        expected = 'https://example.com/path?q=_test_'  # Quotes should be sanitized
        assert str(url_sanitized) == expected
        assert f"{url_sanitized}" == expected