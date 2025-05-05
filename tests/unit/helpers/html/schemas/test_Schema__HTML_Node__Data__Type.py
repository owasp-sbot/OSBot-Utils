from unittest                                                             import TestCase
from osbot_utils.helpers.html.schemas.Schema__HTML_Node__Data__Type       import Schema__HTML_Node__Data__Type

class test_Schema__HTML_Node__Data__Type(TestCase):

    def test_enum_values(self):
        text_type = Schema__HTML_Node__Data__Type.TEXT
        assert text_type.value              == 'text'
        assert str(text_type)               == 'Schema__HTML_Node__Data__Type.TEXT'
        assert text_type.name               == 'TEXT'

    def test_enum_membership(self):
        assert 'TEXT' in Schema__HTML_Node__Data__Type.__members__
        assert len(Schema__HTML_Node__Data__Type.__members__) == 1

    def test_enum_iteration(self):
        types = list(Schema__HTML_Node__Data__Type)
        assert len(types)                   == 1
        assert types[0]                     == Schema__HTML_Node__Data__Type.TEXT
        assert types[0].value               == 'text'