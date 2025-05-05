from unittest                                                             import TestCase

from osbot_utils.helpers.html.Html__To__Html_Dict import STRING__SCHEMA_TEXT
from osbot_utils.helpers.html.schemas.Schema__HTML_Node__Data             import Schema__HTML_Node__Data
from osbot_utils.helpers.html.schemas.Schema__HTML_Node__Data__Type       import Schema__HTML_Node__Data__Type
from osbot_utils.utils.Objects                                            import __

class test_Schema__HTML_Node__Data(TestCase):

    def setUp(self):
        self.node_data = Schema__HTML_Node__Data()

    def test__init__(self):
        with self.node_data as _:
            assert type(_      )            is Schema__HTML_Node__Data
            assert type(_.data )            is str
            assert type(_.type )            is Schema__HTML_Node__Data__Type
            assert _.data                   == ""
            assert _.type                   == Schema__HTML_Node__Data__Type.TEXT
            assert _.json()                 == {'data': '', 'type': STRING__SCHEMA_TEXT}
            assert _.obj ()                 == __(data='', type=Schema__HTML_Node__Data__Type.TEXT.name)

    def test__init__with_params(self):
        data_content = "Sample text content"
        data_type    = Schema__HTML_Node__Data__Type.TEXT
        node_data    = Schema__HTML_Node__Data(data=data_content, type=data_type)
        assert node_data.data               == data_content
        assert node_data.type               == data_type
        assert node_data.type.value         == 'text'

    def test_empty_data(self):
        node_data = Schema__HTML_Node__Data(data="")
        assert node_data.data               == ""

    def test_special_characters(self):
        special_data = "Line1\nLine2\nLine3\tTab"
        node_data    = Schema__HTML_Node__Data(data=special_data)
        assert node_data.data               == special_data

    def test_html_entities(self):
        html_content = "This &amp; that &lt;tag&gt;"
        node_data    = Schema__HTML_Node__Data(data=html_content)
        assert node_data.data               == html_content