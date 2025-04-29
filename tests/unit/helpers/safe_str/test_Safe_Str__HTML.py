import re
from unittest import TestCase

from osbot_utils.helpers.safe_str.Safe_Str                  import Safe_Str
from osbot_utils.helpers.safe_str.Safe_Str__HTML             import Safe_Str__HTML, TYPE_SAFE_STR__HTML__REGEX, TYPE_SAFE_STR__HTML__MAX_LENGTH
from osbot_utils.utils.Objects                              import base_types


class test_Safe_Str__HTML(TestCase):

    def test_Safe_Str__HTML_class(self):
        safe_str_html = Safe_Str__HTML()
        assert type      (safe_str_html)      == Safe_Str__HTML
        assert base_types(safe_str_html)      == [Safe_Str, str, object]
        assert safe_str_html.max_length       == TYPE_SAFE_STR__HTML__MAX_LENGTH
        assert safe_str_html.regex            == re.compile(TYPE_SAFE_STR__HTML__REGEX)
        assert safe_str_html.replacement_char == '_'