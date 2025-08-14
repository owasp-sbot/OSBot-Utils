import re
from unittest                                                     import TestCase
from osbot_utils.type_safe.primitives.safe_str.Safe_Str           import Safe_Str
from osbot_utils.type_safe.Type_Safe__Primitive                   import Type_Safe__Primitive
from osbot_utils.type_safe.primitives.safe_str.web.Safe_Str__Html import Safe_Str__Html, TYPE_SAFE_STR__HTML__MAX_LENGTH, TYPE_SAFE_STR__HTML__REGEX
from osbot_utils.utils.Objects                                    import base_types


class test_Safe_Str__Html(TestCase):

    def test_Safe_Str__HTML_class(self):
        safe_str_html = Safe_Str__Html()
        assert type      (safe_str_html)      == Safe_Str__Html
        assert base_types(safe_str_html)      == [Safe_Str, Type_Safe__Primitive, str, object, object]
        assert safe_str_html.max_length       == TYPE_SAFE_STR__HTML__MAX_LENGTH
        assert safe_str_html.regex            == re.compile(TYPE_SAFE_STR__HTML__REGEX)
        assert safe_str_html.replacement_char == '_'