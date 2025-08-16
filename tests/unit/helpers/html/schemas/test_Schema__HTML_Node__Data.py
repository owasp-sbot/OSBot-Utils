from unittest                                                       import TestCase
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict      import STRING__SCHEMA_TEXT
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data       import Schema__Html_Node__Data
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data__Type import Schema__Html_Node__Data__Type
from osbot_utils.utils.Objects                                      import __

class test_Schema__Html_Node__Data(TestCase):

    def setUp(self):
        self.node_data = Schema__Html_Node__Data()

    def test__init__(self):                                                     # Test basic initialization
        with self.node_data as _:
            assert type(_)       is Schema__Html_Node__Data
            assert type(_.data)  is str
            assert type(_.type)  is Schema__Html_Node__Data__Type
            assert _.data        == ""
            assert _.type        == Schema__Html_Node__Data__Type.TEXT
            assert _.position    == 0                                           # Default position
            expected_json        =  { 'data'     : ''                 ,
                                     'type'     : STRING__SCHEMA_TEXT ,
                                     'position' : 0                   }
            assert _.json()      == expected_json
            assert _.obj()       == __(data     = ''                                         ,
                                      type     = Schema__Html_Node__Data__Type.TEXT.name    ,
                                      position = 0                                           )

    def test__init__with_params(self):                                          # Test initialization with parameters
        data_content = "Sample text content"
        data_type    = Schema__Html_Node__Data__Type.TEXT
        node_data    = Schema__Html_Node__Data(data     = data_content ,
                                              type     = data_type     ,
                                              position = 5             )
        assert node_data.data           == data_content
        assert node_data.type           == data_type
        assert node_data.type.value     == 'text'
        assert node_data.position       == 5

    def test_empty_data(self):                                                  # Test empty data handling
        node_data = Schema__Html_Node__Data(data = "", position = 0)
        assert node_data.data == ""

    def test_special_characters(self):                                          # Test special character handling
        special_data = "Line1\nLine2\nLine3\tTab"
        node_data    = Schema__Html_Node__Data(data = special_data, position = 1)
        assert node_data.data == special_data

    def test_html_entities(self):                                               # Test HTML entity preservation
        html_content = "This &amp; that &lt;tag&gt;"
        node_data    = Schema__Html_Node__Data(data = html_content, position = 2)
        assert node_data.data == html_content