import pytest
from unittest                                                                       import TestCase
from osbot_utils.type_safe.primitives.domains.network.safe_str.Safe_Str__Domain     import Safe_Str__Domain, TYPE_SAFE_STR__DOMAIN__MAX_LENGTH


class test_Safe_Str__Domain(TestCase):

    def test_init(self):
        assert Safe_Str__Domain() == ''

    def test_basic_domains(self):
        """Test basic domain validation"""
        assert Safe_Str__Domain('example.com'          ) == 'example.com'
        assert Safe_Str__Domain('example.org'          ) == 'example.org'
        assert Safe_Str__Domain('example.net'          ) == 'example.net'
        assert Safe_Str__Domain('test.co.uk'           ) == 'test.co.uk'
        assert Safe_Str__Domain('site.com.br'          ) == 'site.com.br'

    def test_domains_with_subdomains(self):
        """Test domains with subdomain levels"""
        assert Safe_Str__Domain('api.example.com'              ) == 'api.example.com'
        assert Safe_Str__Domain('www.example.com'              ) == 'www.example.com'
        assert Safe_Str__Domain('mail.example.com'             ) == 'mail.example.com'
        assert Safe_Str__Domain('api.v2.example.com'           ) == 'api.v2.example.com'
        assert Safe_Str__Domain('deep.sub.domain.example.com'  ) == 'deep.sub.domain.example.com'

    def test_domains_with_numbers(self):
        """Test domains with numeric components"""
        assert Safe_Str__Domain('api2.example.com'     ) == 'api2.example.com'
        assert Safe_Str__Domain('server123.example.com') == 'server123.example.com'
        assert Safe_Str__Domain('v2.api.example.com'   ) == 'v2.api.example.com'
        assert Safe_Str__Domain('123.example.com'      ) == '123.example.com'
        assert Safe_Str__Domain('test1.test2.com'      ) == 'test1.test2.com'

    def test_domains_with_hyphens(self):
        """Test domains with hyphens (valid placement)"""
        assert Safe_Str__Domain('my-site.com'           ) == 'my-site.com'
        assert Safe_Str__Domain('api-server.example.com') == 'api-server.example.com'
        assert Safe_Str__Domain('my-cool-site.co.uk'    ) == 'my-cool-site.co.uk'
        assert Safe_Str__Domain('sub-domain.example.com') == 'sub-domain.example.com'

    def test_localhost(self):
        """Test localhost as special case"""
        assert Safe_Str__Domain('localhost') == 'localhost'

    def test_whitespace_handling(self):
        """Test trimming of leading/trailing whitespace"""
        assert Safe_Str__Domain('  example.com  '      ) == 'example.com'
        assert Safe_Str__Domain('\texample.com\n'      ) == 'example.com'
        assert Safe_Str__Domain('  api.example.com  '  ) == 'api.example.com'

    def test_empty_values(self):
        """Test that empty and None values are handled correctly"""
        assert Safe_Str__Domain(None) == ''
        assert Safe_Str__Domain(''  ) == ''

    def test_invalid_missing_dot(self):
        """Test that domains without dots are rejected (except localhost)"""
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('example')
        assert "must contain at least one dot" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('single')
        assert "must contain at least one dot" in str(exc_info.value)

    def test_invalid_hyphen_placement(self):
        """Test that hyphens at start/end of labels are rejected"""
        # Leading hyphen
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('-example.com')
        assert "in Safe_Str__Domain, value does not match required pattern" in str(exc_info.value)

        # Trailing hyphen
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('example-.com')
        assert "in Safe_Str__Domain, value does not match required pattern" in str(exc_info.value)

        # Hyphen in subdomain label
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('-api.example.com')
        assert "in Safe_Str__Domain, value does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('api-.example.com')
        assert "in Safe_Str__Domain, value does not match required pattern" in str(exc_info.value)

    def test_invalid_with_scheme(self):
        """Test that domains with schemes are rejected"""
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('https://example.com')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('http://example.com')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('ftp://example.com')
        assert "does not match required pattern" in str(exc_info.value)

    def test_invalid_with_port(self):
        """Test that domains with ports are rejected"""
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('example.com:8080')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('api.example.com:443')
        assert "does not match required pattern" in str(exc_info.value)

    def test_invalid_with_path(self):
        """Test that domains with paths are rejected"""
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('example.com/path')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('example.com/api/v1')
        assert "does not match required pattern" in str(exc_info.value)

    def test_invalid_special_characters(self):
        """Test that invalid special characters are rejected"""
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('example_com.com')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('example@site.com')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('example.com?query')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('example.com#fragment')
        assert "does not match required pattern" in str(exc_info.value)

    def test_invalid_spaces(self):
        """Test that domains with spaces are rejected"""
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('example .com')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('my site.com')
        assert "does not match required pattern" in str(exc_info.value)

    def test_invalid_label_length(self):
        """Test that labels exceeding 63 characters are rejected"""
        # Valid: 63 characters
        valid_label = 'a' * 63
        assert Safe_Str__Domain(f'{valid_label}.com') == f'{valid_label}.com'

        # Invalid: 64 characters
        with pytest.raises(ValueError) as exc_info:
            invalid_label = 'a' * 64
            Safe_Str__Domain(f'{invalid_label}.com')
        assert "in Safe_Str__Domain, value does not match required pattern" in str(exc_info.value)

    def test_invalid_empty_label(self):
        """Test that empty labels (consecutive dots) are rejected"""
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('example..com')
        assert "in Safe_Str__Domain, value does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('.example.com')
        assert "in Safe_Str__Domain, value does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('example.com.')
        assert "in Safe_Str__Domain, value does not match required pattern" in str(exc_info.value)

    def test_max_length_validation(self):
        """Test max length enforcement (253 characters per RFC 1035)"""
        # Within limit: 253 characters
        # Create domain with multiple 63-char labels
        label = 'a' * 63
        valid_domain = f'{label}.{label}.{label}.com'  # ~195 chars
        assert len(Safe_Str__Domain(valid_domain)) > 0

        # Exceeds limit: > 253 characters
        with pytest.raises(ValueError) as exc_info:
            long_domain = '.'.join(['a' * 63 for _ in range(5)])  # ~320 chars
            Safe_Str__Domain(long_domain)
        assert f"exceeds maximum length of {TYPE_SAFE_STR__DOMAIN__MAX_LENGTH}" in str(exc_info.value)

    def test_common_domain_patterns(self):
        """Test common real-world domain patterns"""
        # Common TLDs
        assert Safe_Str__Domain('example.com'      ) == 'example.com'
        assert Safe_Str__Domain('example.org'      ) == 'example.org'
        assert Safe_Str__Domain('example.net'      ) == 'example.net'
        assert Safe_Str__Domain('example.io'       ) == 'example.io'
        assert Safe_Str__Domain('example.dev'      ) == 'example.dev'

        # Country code TLDs
        assert Safe_Str__Domain('example.co.uk'    ) == 'example.co.uk'
        assert Safe_Str__Domain('example.com.br'   ) == 'example.com.br'
        assert Safe_Str__Domain('example.de'       ) == 'example.de'
        assert Safe_Str__Domain('example.fr'       ) == 'example.fr'

        # API domains
        assert Safe_Str__Domain('api.github.com'   ) == 'api.github.com'
        assert Safe_Str__Domain('api.stripe.com'   ) == 'api.stripe.com'
        assert Safe_Str__Domain('graph.facebook.com') == 'graph.facebook.com'

        # Subdomains
        assert Safe_Str__Domain('www.example.com'  ) == 'www.example.com'
        assert Safe_Str__Domain('mail.google.com'  ) == 'mail.google.com'
        assert Safe_Str__Domain('docs.python.org'  ) == 'docs.python.org'

    def test_development_domains(self):
        """Test development and testing domain patterns"""
        assert Safe_Str__Domain('localhost'            ) == 'localhost'
        assert Safe_Str__Domain('dev.example.com'      ) == 'dev.example.com'
        assert Safe_Str__Domain('staging.example.com'  ) == 'staging.example.com'
        assert Safe_Str__Domain('test.example.com'     ) == 'test.example.com'

    def test_string_representation(self):
        """Test string conversion methods"""
        domain = Safe_Str__Domain('api.example.com')

        assert str(domain)  == 'api.example.com'
        assert repr(domain) == "Safe_Str__Domain('api.example.com')"
        assert f"Domain: {domain}" == "Domain: api.example.com"

    def test_equality_and_comparison(self):
        """Test domain equality"""
        domain1 = Safe_Str__Domain('example.com')
        domain2 = Safe_Str__Domain('example.com')
        domain3 = Safe_Str__Domain('other.com')

        assert domain1 == domain2
        assert domain1 == 'example.com'
        assert domain1 != domain3

    def test_immutability(self):
        """Test that domains are immutable"""
        domain1 = Safe_Str__Domain('example.com')
        domain2 = Safe_Str__Domain('example.com')

        assert domain1 == domain2
        assert domain1 is not domain2
        assert hash(domain1) == hash(domain2)

    def test_case_sensitivity(self):
        """Test domain case handling"""
        # Domains are case-insensitive in practice, but we preserve case
        assert Safe_Str__Domain('Example.Com'  ) == 'Example.Com'
        assert Safe_Str__Domain('API.EXAMPLE.COM') == 'API.EXAMPLE.COM'
        assert Safe_Str__Domain('api.example.com') == 'api.example.com'

        # They should be equal when compared (case-insensitive comparison)
        # Note: This depends on whether you want case-sensitive or case-insensitive
        # For now, they're different string values
        domain_upper = Safe_Str__Domain('EXAMPLE.COM')
        domain_lower = Safe_Str__Domain('example.com')
        assert domain_upper != domain_lower  # Different as strings

    def test_edge_cases(self):
        """Test various edge cases"""
        # Single character labels
        assert Safe_Str__Domain('a.b.c') == 'a.b.c'

        # Maximum length label (63 chars)
        max_label = 'a' * 63
        assert Safe_Str__Domain(f'{max_label}.com') == f'{max_label}.com'

        # Many subdomains
        many_subs = 'a.b.c.d.e.f.g.h.example.com'
        assert Safe_Str__Domain(many_subs) == many_subs

        # Numeric TLD (technically valid)
        assert Safe_Str__Domain('example.123') == 'example.123'

        # All numeric label (valid)
        assert Safe_Str__Domain('123.456.789') == '123.456.789'

    def test_internationalized_domains(self):
        """Test that non-ASCII characters are rejected (punycode should be used)"""
        # These should fail - IDNs must be in punycode format
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('café.com')
        assert "does not match required pattern" in str(exc_info.value)

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('日本.jp')
        assert "does not match required pattern" in str(exc_info.value)

        # Punycode versions should work
        assert Safe_Str__Domain('xn--caf-dma.com') == 'xn--caf-dma.com'  # café.com in punycode

    def test_common_tlds(self):
        """Test domains with various common TLDs"""
        # Generic TLDs
        assert Safe_Str__Domain('site.com'     ) == 'site.com'
        assert Safe_Str__Domain('site.net'     ) == 'site.net'
        assert Safe_Str__Domain('site.org'     ) == 'site.org'
        assert Safe_Str__Domain('site.info'    ) == 'site.info'
        assert Safe_Str__Domain('site.biz'     ) == 'site.biz'

        # New TLDs
        assert Safe_Str__Domain('site.io'      ) == 'site.io'
        assert Safe_Str__Domain('site.ai'      ) == 'site.ai'
        assert Safe_Str__Domain('site.dev'     ) == 'site.dev'
        assert Safe_Str__Domain('site.app'     ) == 'site.app'
        assert Safe_Str__Domain('site.cloud'   ) == 'site.cloud'

    def test_security_patterns(self):
        """Test that potentially malicious patterns are rejected"""
        # SQL injection attempts
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain("example.com'; DROP TABLE--")
        assert "does not match required pattern" in str(exc_info.value)

        # XSS attempts
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('example.com<script>')
        assert "does not match required pattern" in str(exc_info.value)

        # Path traversal
        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Domain('../etc/passwd')
        assert "does not match required pattern" in str(exc_info.value)