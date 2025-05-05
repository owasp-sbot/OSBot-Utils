from unittest                                                             import TestCase
from osbot_utils.helpers.html.Html__To__Html_Dict                         import STRING__SCHEMA_TEXT, STRING__SCHEMA_NODES
from osbot_utils.helpers.html.schemas.Schema__HTML_Document               import Schema__HTML_Document
from osbot_utils.helpers.html.schemas.Schema__HTML_Node                   import Schema__HTML_Node
from osbot_utils.helpers.html.schemas.Schema__HTML_Node__Data             import Schema__HTML_Node__Data
from osbot_utils.helpers.html.schemas.Schema__HTML_Node__Data__Type       import Schema__HTML_Node__Data__Type
from osbot_utils.utils.Objects                                            import __

class test_Schema__HTML_Document(TestCase):

    def setUp(self):
        self.document = Schema__HTML_Document()

    def test__init__(self):
        with self.document as _:
            assert type(_      )  is Schema__HTML_Document
            assert type(_.root_node)  is Schema__HTML_Node
            assert _.json()       == { 'timestamp': _.timestamp, 'root_node':{'attrs': {}, 'nodes': [], 'tag': ''}}
            assert _.obj ()       == __(timestamp=_.timestamp, root_node =__(attrs=__(), nodes=[], tag=''))
            
    def test__init__with_params(self):
        node_child   = Schema__HTML_Node()
        document     = Schema__HTML_Document(root_node = node_child   )
        assert document.root_node            == node_child

    def test_complete_html_structure(self):
        title_text    = Schema__HTML_Node__Data(data = 'Test Page'   , type  = Schema__HTML_Node__Data__Type.TEXT)
        title_node    = Schema__HTML_Node      (tag  = 'title'       , nodes = [title_text])
        meta_node     = Schema__HTML_Node      (tag  = 'meta'        , attrs = {'charset': 'utf-8'})
        body_text     = Schema__HTML_Node__Data(data = 'Hello World' , type  = Schema__HTML_Node__Data__Type.TEXT)
        paragraph     = Schema__HTML_Node      (tag  = 'p'           , nodes = [body_text])
        body_node     = Schema__HTML_Node      (tag  = 'body'        , nodes = [paragraph])
        root_node     = Schema__HTML_Node      (attrs= {'lang': 'en'}, nodes = [title_node, meta_node, body_node])
        html_document = Schema__HTML_Document  (root_node=root_node)

        root_node = html_document.root_node
        assert root_node.attrs['lang']             == 'en'
        assert len(root_node.nodes)                == 3
        assert root_node.nodes[0].tag              == 'title'
        assert root_node.nodes[0].nodes[0].data    == 'Test Page'
        assert root_node.nodes[1].tag              == 'meta'
        assert root_node.nodes[1].attrs['charset'] == 'utf-8'
        assert root_node.nodes[2].tag              == 'body'
        assert root_node.nodes[2].nodes[0].tag     == 'p'

    def test_nested_structure_with_mixed_content(self):
        text_1       = Schema__HTML_Node__Data(data='Start', type=Schema__HTML_Node__Data__Type.TEXT)
        span_node    = Schema__HTML_Node      (tag='span', attrs={'class': 'highlight'})
        text_2       = Schema__HTML_Node__Data(data='End', type=Schema__HTML_Node__Data__Type.TEXT)
        paragraph    = Schema__HTML_Node      (tag='p', nodes=[text_1, span_node, text_2])
        root_node    = Schema__HTML_Node      (nodes=[paragraph])

        assert len(root_node.nodes)                    == 1
        assert root_node.nodes[0].tag                  == 'p'
        assert len(root_node.nodes[0].nodes)        == 3
        assert root_node.nodes[0].nodes[0].data     == 'Start'
        assert root_node.nodes[0].nodes[1].tag      == 'span'
        assert root_node.nodes[0].nodes[2].data     == 'End'

    def test_deep_nesting_structure(self):
        deepest_text = Schema__HTML_Node__Data(data='Deeply nested', type=Schema__HTML_Node__Data__Type.TEXT)
        deepest_span = Schema__HTML_Node      (tag='span', nodes=[deepest_text])
        div_level_3  = Schema__HTML_Node      (tag='div', nodes=[deepest_span])
        div_level_2  = Schema__HTML_Node      (tag='div', nodes=[div_level_3])
        div_level_1  = Schema__HTML_Node      (tag='div', nodes=[div_level_2])
        root_node    = Schema__HTML_Node  (nodes=[div_level_1])

        # Test deep access
        nested_span = root_node.nodes[0].nodes[0].nodes[0].nodes[0]
        assert nested_span.tag                           == 'span'
        assert nested_span.nodes[0].data              == 'Deeply nested'

    def test_html_form_structure(self):
        input_attrs  = {'type': STRING__SCHEMA_TEXT, 'name': 'username', 'required': 'true'}
        label_text   = Schema__HTML_Node__Data(data='Username:', type=Schema__HTML_Node__Data__Type.TEXT)
        label_node   = Schema__HTML_Node      (tag='label', attrs={'for': 'username'}, nodes=[label_text])
        input_node   = Schema__HTML_Node      (tag='input', attrs=input_attrs)
        submit_text  = Schema__HTML_Node__Data(data='Submit', type=Schema__HTML_Node__Data__Type.TEXT)
        submit_btn   = Schema__HTML_Node      (tag='button', attrs={'type': 'submit'}, nodes=[submit_text])
        form_node    = Schema__HTML_Node      (tag='form', nodes=[label_node, input_node, submit_btn])
        root_node    = Schema__HTML_Node  (nodes=[form_node])

        assert root_node.nodes[0].tag                              == 'form'
        assert root_node.nodes[0].nodes[0].tag                  == 'label'
        assert root_node.nodes[0].nodes[1].tag                  == 'input'
        assert root_node.nodes[0].nodes[1].attrs['type']        == STRING__SCHEMA_TEXT
        assert root_node.nodes[0].nodes[2].nodes[0].data     == 'Submit'