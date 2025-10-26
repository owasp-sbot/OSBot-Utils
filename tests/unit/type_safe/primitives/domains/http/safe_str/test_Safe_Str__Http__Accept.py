import pytest
from unittest                                                                   import TestCase
from osbot_utils.type_safe.primitives.domains.http.safe_str.Safe_Str__Http__Accept import Safe_Str__Http__Accept


class test_Safe_Str__Http__Accept(TestCase):

    def test__init__(self):                                                             # Test Safe_Str__Http__Accept initialization
        accept = Safe_Str__Http__Accept('application/json')
        assert type(accept)           is Safe_Str__Http__Accept
        assert str(accept)            == 'application/json'
        assert accept                 == 'application/json'

    def test__simple_mime_types(self):                                                  # Test simple MIME type values
        assert Safe_Str__Http__Accept('text/html'            ) == 'text/html'
        assert Safe_Str__Http__Accept('application/json'     ) == 'application/json'
        assert Safe_Str__Http__Accept('application/xml'      ) == 'application/xml'
        assert Safe_Str__Http__Accept('image/png'            ) == 'image/png'
        assert Safe_Str__Http__Accept('image/jpeg'           ) == 'image/jpeg'
        assert Safe_Str__Http__Accept('video/mp4'            ) == 'video/mp4'
        assert Safe_Str__Http__Accept('audio/mpeg'           ) == 'audio/mpeg'
        assert Safe_Str__Http__Accept('text/plain'           ) == 'text/plain'
        assert Safe_Str__Http__Accept('text/css'             ) == 'text/css'
        assert Safe_Str__Http__Accept('application/javascript') == 'application/javascript'

    def test__wildcard_types(self):                                                     # Test wildcard MIME types
        assert Safe_Str__Http__Accept('*/*'                  ) == '*/*'
        assert Safe_Str__Http__Accept('text/*'               ) == 'text/*'
        assert Safe_Str__Http__Accept('application/*'        ) == 'application/*'
        assert Safe_Str__Http__Accept('image/*'              ) == 'image/*'
        assert Safe_Str__Http__Accept('audio/*'              ) == 'audio/*'
        assert Safe_Str__Http__Accept('video/*'              ) == 'video/*'

    def test__quality_parameters(self):                                                 # Test quality (q) parameter values
        assert Safe_Str__Http__Accept('text/html;q=0.9'      ) == 'text/html;q=0.9'
        assert Safe_Str__Http__Accept('application/json;q=1.0') == 'application/json;q=1.0'
        assert Safe_Str__Http__Accept('*/*;q=0.8'            ) == '*/*;q=0.8'
        assert Safe_Str__Http__Accept('text/plain;q=0.5'     ) == 'text/plain;q=0.5'
        assert Safe_Str__Http__Accept('image/webp;q=0.95'    ) == 'image/webp;q=0.95'

    def test__multiple_mime_types(self):                                                # Test multiple MIME types in one header
        assert Safe_Str__Http__Accept('text/html,application/json') == 'text/html,application/json'
        assert Safe_Str__Http__Accept('text/html, application/json') == 'text/html, application/json'
        assert Safe_Str__Http__Accept('text/html,application/xml,application/json') == 'text/html,application/xml,application/json'

    def test__complex_accept_headers(self):                                             # Test complex real-world Accept headers
        browser_accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        assert Safe_Str__Http__Accept(browser_accept         ) == browser_accept

        api_accept = 'application/json, text/plain, */*'
        assert Safe_Str__Http__Accept(api_accept             ) == api_accept

        chrome_accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8'
        assert Safe_Str__Http__Accept(chrome_accept          ) == chrome_accept

    def test__with_charset_parameter(self):                                             # Test MIME types with charset parameter
        assert Safe_Str__Http__Accept('text/html; charset=utf-8') == 'text/html; charset=utf-8'
        assert Safe_Str__Http__Accept('application/json; charset=utf-8') == 'application/json; charset=utf-8'
        assert Safe_Str__Http__Accept('text/plain; charset=iso-8859-1') == 'text/plain; charset=iso-8859-1'

    def test__vendor_specific_mime_types(self):                                         # Test vendor-specific MIME types
        assert Safe_Str__Http__Accept('application/vnd.api+json') == 'application/vnd.api+json'
        assert Safe_Str__Http__Accept('application/vnd.ms-excel') == 'application/vnd.ms-excel'
        assert Safe_Str__Http__Accept('application/ld+json'  ) == 'application/ld+json'
        assert Safe_Str__Http__Accept('application/vnd.github.v3+json') == 'application/vnd.github.v3+json'

    def test__decimal_quality_values(self):                                             # Test various quality value decimal formats
        assert Safe_Str__Http__Accept('text/html;q=1'        ) == 'text/html;q=1'
        assert Safe_Str__Http__Accept('text/html;q=0.9'      ) == 'text/html;q=0.9'
        assert Safe_Str__Http__Accept('text/html;q=0.99'     ) == 'text/html;q=0.99'
        assert Safe_Str__Http__Accept('text/html;q=0.999'    ) == 'text/html;q=0.999'
        assert Safe_Str__Http__Accept('text/html;q=0'        ) == 'text/html;q=0'

    def test__level_parameters(self):                                                   # Test level parameter in Accept headers
        assert Safe_Str__Http__Accept('text/html; level=1'   ) == 'text/html; level=1'
        assert Safe_Str__Http__Accept('text/html; level=2; q=0.9') == 'text/html; level=2; q=0.9'

    def test__whitespace_handling(self):                                                # Test trim_whitespace = True
        assert Safe_Str__Http__Accept('  text/html  '       ) == 'text/html'
        assert Safe_Str__Http__Accept('application/json  '  ) == 'application/json'
        assert Safe_Str__Http__Accept('  */*'               ) == '*/*'

    def test__numeric_conversion(self):                                                 # Test conversion from numeric types
        assert Safe_Str__Http__Accept(12345                  ) == '12345'
        assert Safe_Str__Http__Accept(999                    ) == '999'

    def test__invalid_characters(self):                                                 # Test regex character replacement
        assert Safe_Str__Http__Accept('text/html<script>'    ) == 'text/html_script_'
        assert Safe_Str__Http__Accept('text@html'            ) == 'text_html'
        assert Safe_Str__Http__Accept('text:html'            ) == 'text_html'
        assert Safe_Str__Http__Accept('application#json'     ) == 'application_json'

    def test__empty_values(self):                                                       # Test allow_empty = True
        assert Safe_Str__Http__Accept(None                   ) == ''
        assert Safe_Str__Http__Accept(''                     ) == ''
        assert Safe_Str__Http__Accept('   '                  ) == ''                    # Spaces only (will be trimmed)

    def test__max_length(self):                                                         # Test TYPE_SAFE_STR__HTTP__ACCEPT__MAX_LENGTH = 512
        valid_512   = 'a' * 512
        invalid_513 = 'a' * 513

        assert Safe_Str__Http__Accept(valid_512              ) == valid_512

        with pytest.raises(ValueError) as exc_info:
            Safe_Str__Http__Accept(invalid_513)
        assert "in Safe_Str__Http__Accept, value exceeds maximum length of 512" in str(exc_info.value)

    def test__special_subtypes(self):                                                   # Test special MIME subtype formats
        assert Safe_Str__Http__Accept('application/x-www-form-urlencoded') == 'application/x-www-form-urlencoded'
        assert Safe_Str__Http__Accept('multipart/form-data'  ) == 'multipart/form-data'
        assert Safe_Str__Http__Accept('text/event-stream'    ) == 'text/event-stream'
        assert Safe_Str__Http__Accept('application/octet-stream') == 'application/octet-stream'

    def test__image_formats(self):                                                      # Test various image format MIME types
        assert Safe_Str__Http__Accept('image/png'            ) == 'image/png'
        assert Safe_Str__Http__Accept('image/jpeg'           ) == 'image/jpeg'
        assert Safe_Str__Http__Accept('image/gif'            ) == 'image/gif'
        assert Safe_Str__Http__Accept('image/webp'           ) == 'image/webp'
        assert Safe_Str__Http__Accept('image/svg+xml'        ) == 'image/svg+xml'
        assert Safe_Str__Http__Accept('image/avif'           ) == 'image/avif'
        assert Safe_Str__Http__Accept('image/apng'           ) == 'image/apng'

    def test__str_and_repr(self):                                                       # Test string representations
        accept = Safe_Str__Http__Accept('application/json')

        assert str(accept)            == 'application/json'
        assert f"{accept}"            == 'application/json'
        assert f"Accept: {accept}"    == 'Accept: application/json'