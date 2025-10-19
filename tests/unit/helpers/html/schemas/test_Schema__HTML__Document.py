from unittest                                                       import TestCase
from osbot_utils.helpers.html.transformers.Html__To__Html_Dict      import STRING__SCHEMA_TEXT, STRING__SCHEMA_NODES
from osbot_utils.helpers.html.schemas.Schema__Html_Document         import Schema__Html_Document
from osbot_utils.helpers.html.schemas.Schema__Html_Node             import Schema__Html_Node
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data       import Schema__Html_Node__Data
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data__Type import Schema__Html_Node__Data__Type
from osbot_utils.testing.__                                         import __

class test_Schema__Html_Document(TestCase):

    def setUp(self):
        self.document = Schema__Html_Document()

    def test__init__(self):                                                     # Test basic initialization
        with self.document as _:
            assert type(_)       is Schema__Html_Document
            assert type(_.root_node) is Schema__Html_Node
            expected_json = { 'timestamp': _.timestamp                      ,
                             'root_node': { 'attrs'      : {}               ,
                                           'child_nodes' : []               ,
                                           'text_nodes'  : []               ,
                                           'tag'         : ''               ,
                                           'position'    : -1               }}
            assert _.json() == expected_json
            assert _.obj()  == __(timestamp = _.timestamp                   ,
                                  root_node = __(attrs       = __()          ,
                                                child_nodes = []            ,
                                                text_nodes  = []            ,
                                                tag         = ''            ,
                                                position    = -1            ))

    def test__init__with_params(self):                                         # Test initialization with parameters
        node_child = Schema__Html_Node()
        document   = Schema__Html_Document(root_node = node_child)
        assert document.root_node == node_child

    def test_complete_html_structure(self):                                    # Test complete HTML document structure
        title_text = Schema__Html_Node__Data(data     = 'Test Page'                                ,
                                            type     = Schema__Html_Node__Data__Type.TEXT         ,
                                            position = 0                                           )
        title_node = Schema__Html_Node      (tag         = 'title'                                 ,
                                            text_nodes  = [title_text]                             ,
                                            child_nodes = []                                       ,
                                            position    = 0                                        )

        meta_node  = Schema__Html_Node      (tag         = 'meta'                                  ,
                                            attrs       = {'charset': 'utf-8'}                     ,
                                            child_nodes = []                                       ,
                                            text_nodes  = []                                       ,
                                            position    = 1                                        )

        body_text  = Schema__Html_Node__Data(data        = 'Hello World'                           ,
                                            type        = Schema__Html_Node__Data__Type.TEXT      ,
                                            position    = 0                                        )
        paragraph  = Schema__Html_Node      (tag         = 'p'                                     ,
                                            child_nodes = []                                       ,
                                            text_nodes  = [body_text]                              ,
                                            position    = 0                                        )
        body_node  = Schema__Html_Node      (tag         = 'body'                                  ,
                                            child_nodes = [paragraph]                              ,
                                            text_nodes  = []                                       ,
                                            position    = 2                                        )

        root_node     = Schema__Html_Node   (attrs       = {'lang': 'en'}                          ,
                                            child_nodes = [title_node, meta_node, body_node]      ,
                                            text_nodes  = []                                       ,
                                            tag         = 'html'                                   ,
                                            position    = -1                                       )
        html_document = Schema__Html_Document(root_node   = root_node                               )

        root_node = html_document.root_node
        assert root_node.attrs['lang']                              == 'en'
        assert len(root_node.child_nodes)                           == 3
        assert root_node.child_nodes[0].tag                        == 'title'
        assert root_node.child_nodes[0].text_nodes[0].data         == 'Test Page'
        assert root_node.child_nodes[1].tag                        == 'meta'
        assert root_node.child_nodes[1].attrs['charset']           == 'utf-8'
        assert root_node.child_nodes[2].tag                        == 'body'
        assert root_node.child_nodes[2].child_nodes[0].tag         == 'p'

    def test_nested_structure_with_mixed_content(self):                        # Test mixed text and element content
        text_1    = Schema__Html_Node__Data(data     = 'Start'                                     ,
                                           type     = Schema__Html_Node__Data__Type.TEXT          ,
                                           position = 0                                            )
        text_2    = Schema__Html_Node__Data(data     = 'End'                                       ,
                                           type     = Schema__Html_Node__Data__Type.TEXT          ,
                                           position = 2                                            )

        span_node = Schema__Html_Node      (tag         = 'span'                                   ,
                                           attrs       = {'class': 'highlight'}                    ,
                                           child_nodes = []                                        ,
                                           text_nodes  = []                                        ,
                                           position    = 1                                         )

        paragraph = Schema__Html_Node      (tag         = 'p'                                      ,
                                           child_nodes = [span_node]                               ,
                                           text_nodes  = [text_1, text_2]                          ,
                                           position    = 0                                         )

        root_node = Schema__Html_Node      (child_nodes = [paragraph]                              ,
                                           text_nodes  = []                                        ,
                                           tag         = 'div'                                     ,
                                           position    = -1                                        )

        assert len(root_node.child_nodes)                         == 1
        assert root_node.child_nodes[0].tag                       == 'p'
        assert len(root_node.child_nodes[0].child_nodes)          == 1
        assert len(root_node.child_nodes[0].text_nodes)           == 2

        text_nodes_by_pos = {t.position: t for t in root_node.child_nodes[0].text_nodes}
        assert text_nodes_by_pos[0].data                          == 'Start'
        assert text_nodes_by_pos[2].data                          == 'End'
        assert root_node.child_nodes[0].child_nodes[0].tag        == 'span'
        assert root_node.child_nodes[0].child_nodes[0].position   == 1

    def test_deep_nesting_structure(self):                                     # Test deeply nested structure
        deepest_text = Schema__Html_Node__Data(data     = 'Deeply nested'                          ,
                                              type     = Schema__Html_Node__Data__Type.TEXT       ,
                                              position = 0                                         )

        deepest_span = Schema__Html_Node      (tag         = 'span'                                ,
                                              text_nodes  = [deepest_text]                         ,
                                              child_nodes = []                                     ,
                                              position    = 0                                      )
        div_level_3  = Schema__Html_Node      (tag         = 'div'                                 ,
                                              child_nodes = [deepest_span]                         ,
                                              text_nodes  = []                                     ,
                                              position    = 0                                      )
        div_level_2  = Schema__Html_Node      (tag         = 'div'                                 ,
                                              child_nodes = [div_level_3]                          ,
                                              text_nodes  = []                                     ,
                                              position    = 0                                      )
        div_level_1  = Schema__Html_Node      (tag         = 'div'                                 ,
                                              child_nodes = [div_level_2]                          ,
                                              text_nodes  = []                                     ,
                                              position    = 0                                      )
        root_node    = Schema__Html_Node      (child_nodes = [div_level_1]                         ,
                                              text_nodes  = []                                     ,
                                              tag         = 'div'                                  ,
                                              position    = -1                                     )

        nested_span = root_node.child_nodes[0].child_nodes[0].child_nodes[0].child_nodes[0]
        assert nested_span.tag                    == 'span'
        assert nested_span.text_nodes[0].data     == 'Deeply nested'

    def test_html_form_structure(self):                                        # Test HTML form structure
        input_attrs  = {'type': STRING__SCHEMA_TEXT, 'name': 'username', 'required': 'true'}

        label_text   = Schema__Html_Node__Data(data     = 'Username:'                              ,
                                              type     = Schema__Html_Node__Data__Type.TEXT       ,
                                              position = 0                                         )
        label_node   = Schema__Html_Node      (tag         = 'label'                               ,
                                              attrs       = {'for': 'username'}                    ,
                                              text_nodes  = [label_text]                           ,
                                              child_nodes = []                                     ,
                                              position    = 0                                      )

        input_node   = Schema__Html_Node      (tag         = 'input'                               ,
                                              attrs       = input_attrs                            ,
                                              child_nodes = []                                     ,
                                              text_nodes  = []                                     ,
                                              position    = 1                                      )

        submit_text  = Schema__Html_Node__Data(data     = 'Submit'                                 ,
                                              type     = Schema__Html_Node__Data__Type.TEXT       ,
                                              position = 0                                         )
        submit_btn   = Schema__Html_Node      (tag         = 'button'                              ,
                                              attrs       = {'type': 'submit'}                     ,
                                              text_nodes  = [submit_text]                          ,
                                              child_nodes = []                                     ,
                                              position    = 2                                      )

        form_node    = Schema__Html_Node      (tag         = 'form'                                ,
                                              child_nodes = [label_node, input_node, submit_btn]   ,
                                              text_nodes  = []                                     ,
                                              position    = 0                                      )

        root_node    = Schema__Html_Node      (child_nodes = [form_node]                           ,
                                              text_nodes  = []                                     ,
                                              tag         = 'div'                                  ,
                                              position    = -1                                     )

        assert root_node.child_nodes[0].tag                                      == 'form'
        assert root_node.child_nodes[0].child_nodes[0].tag                       == 'label'
        assert root_node.child_nodes[0].child_nodes[1].tag                       == 'input'
        assert root_node.child_nodes[0].child_nodes[1].attrs['type']             == STRING__SCHEMA_TEXT
        assert root_node.child_nodes[0].child_nodes[2].text_nodes[0].data        == 'Submit'