from unittest                                                             import TestCase

from osbot_utils.helpers.html.Html__To__Html_Dict import STRING__SCHEMA_TEXT
from osbot_utils.helpers.html.schemas.Schema__HTML_Document               import Schema__HTML_Document
from osbot_utils.helpers.html.schemas.Schema__HTML_Node                   import Schema__HTML_Node
from osbot_utils.helpers.html.schemas.Schema__HTML_Node__Data             import Schema__HTML_Node__Data
from osbot_utils.helpers.html.schemas.Schema__HTML_Node__Data__Type       import Schema__HTML_Node__Data__Type
from osbot_utils.type_safe.Type_Safe__Dict                                import Type_Safe__Dict
from osbot_utils.type_safe.Type_Safe__List                                import Type_Safe__List
from osbot_utils.utils.Objects                                            import __

class test_Schema__HTML_Document(TestCase):

    def setUp(self):
        self.document = Schema__HTML_Document()

    def test__init__(self):
        with self.document as _:
            assert type(_       )           is Schema__HTML_Document
            assert type(_.attrs )           is Type_Safe__Dict
            assert type(_.children)         is Type_Safe__List
            assert _.attrs                  == {}
            assert _.children               == []
            assert _.json()                 == {'attrs': {}, 'children': []}
            assert _.obj ()                 == __(attrs=__(), children=[])
            
    def test__init__with_params(self):
        node_child   = Schema__HTML_Node()
        document     = Schema__HTML_Document(attrs    = {'lang': 'en'}                    ,
                                              children = [node_child              ])
        assert document.attrs               == {'lang': 'en'}
        assert document.children            == [node_child]
        assert len(document.children)       == 1
        assert document.children[0]         == node_child
        assert type(document.children[0])   is Schema__HTML_Node

    def test_empty_attributes(self):
        document = Schema__HTML_Document(attrs={})
        assert document.attrs               == {}

    def test_empty_children(self):
        document = Schema__HTML_Document(children=[])
        assert document.children            == []

    def test_multiple_children(self):
        node_1     = Schema__HTML_Node(tag='title')
        node_2     = Schema__HTML_Node(tag='meta' )
        document   = Schema__HTML_Document(children=[node_1, node_2])
        assert len(document.children)       == 2
        assert document.children[0]         == node_1
        assert document.children[1]         == node_2

    def test_complete_html_structure(self):
        title_text    = Schema__HTML_Node__Data(data = 'Test Page'   , type     = Schema__HTML_Node__Data__Type.TEXT)
        title_node    = Schema__HTML_Node      (tag  = 'title'       , children = [title_text])
        meta_node     = Schema__HTML_Node      (tag  = 'meta'        , attrs    = {'charset': 'utf-8'})
        body_text     = Schema__HTML_Node__Data(data = 'Hello World' , type     = Schema__HTML_Node__Data__Type.TEXT)
        paragraph     = Schema__HTML_Node      (tag  = 'p'           , children = [body_text])
        body_node     = Schema__HTML_Node      (tag  = 'body'        , children = [paragraph])
        html_document = Schema__HTML_Document  (attrs= {'lang': 'en'}, children = [title_node, meta_node, body_node])

        assert html_document.attrs['lang']               == 'en'
        assert len(html_document.children)               == 3
        assert html_document.children[0].tag             == 'title'
        assert html_document.children[0].children[0].data == 'Test Page'
        assert html_document.children[1].tag             == 'meta'
        assert html_document.children[1].attrs['charset'] == 'utf-8'
        assert html_document.children[2].tag             == 'body'
        assert html_document.children[2].children[0].tag  == 'p'

    def test_nested_structure_with_mixed_content(self):
        text_1       = Schema__HTML_Node__Data(data='Start', type=Schema__HTML_Node__Data__Type.TEXT)
        span_node    = Schema__HTML_Node      (tag='span', attrs={'class': 'highlight'})
        text_2       = Schema__HTML_Node__Data(data='End', type=Schema__HTML_Node__Data__Type.TEXT)
        paragraph    = Schema__HTML_Node      (tag='p', children=[text_1, span_node, text_2])
        document     = Schema__HTML_Document  (children=[paragraph])

        assert len(document.children)                    == 1
        assert document.children[0].tag                  == 'p'
        assert len(document.children[0].children)        == 3
        assert document.children[0].children[0].data     == 'Start'
        assert document.children[0].children[1].tag      == 'span'
        assert document.children[0].children[2].data     == 'End'

    def test_deep_nesting_structure(self):
        deepest_text = Schema__HTML_Node__Data(data='Deeply nested', type=Schema__HTML_Node__Data__Type.TEXT)
        deepest_span = Schema__HTML_Node      (tag='span', children=[deepest_text])
        div_level_3  = Schema__HTML_Node      (tag='div', children=[deepest_span])
        div_level_2  = Schema__HTML_Node      (tag='div', children=[div_level_3])
        div_level_1  = Schema__HTML_Node      (tag='div', children=[div_level_2])
        document     = Schema__HTML_Document  (children=[div_level_1])

        # Test deep access
        nested_span = document.children[0].children[0].children[0].children[0]
        assert nested_span.tag                           == 'span'
        assert nested_span.children[0].data              == 'Deeply nested'

    def test_html_form_structure(self):
        input_attrs  = {'type': STRING__SCHEMA_TEXT, 'name': 'username', 'required': 'true'}
        label_text   = Schema__HTML_Node__Data(data='Username:', type=Schema__HTML_Node__Data__Type.TEXT)
        label_node   = Schema__HTML_Node      (tag='label', attrs={'for': 'username'}, children=[label_text])
        input_node   = Schema__HTML_Node      (tag='input', attrs=input_attrs)
        submit_text  = Schema__HTML_Node__Data(data='Submit', type=Schema__HTML_Node__Data__Type.TEXT)
        submit_btn   = Schema__HTML_Node      (tag='button', attrs={'type': 'submit'}, children=[submit_text])
        form_node    = Schema__HTML_Node      (tag='form', children=[label_node, input_node, submit_btn])
        document     = Schema__HTML_Document  (children=[form_node])

        assert document.children[0].tag                              == 'form'
        assert document.children[0].children[0].tag                  == 'label'
        assert document.children[0].children[1].tag                  == 'input'
        assert document.children[0].children[1].attrs['type']        == STRING__SCHEMA_TEXT
        assert document.children[0].children[2].children[0].data     == 'Submit'