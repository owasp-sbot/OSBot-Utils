from unittest                                                       import TestCase
from osbot_utils.helpers.html.schemas.Schema__Html_Node             import Schema__Html_Node
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data       import Schema__Html_Node__Data
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data__Type import Schema__Html_Node__Data__Type
from osbot_utils.type_safe.Type_Safe__Dict                          import Type_Safe__Dict
from osbot_utils.type_safe.Type_Safe__List                          import Type_Safe__List
from osbot_utils.utils.Objects                                      import __

class test_Schema__Html_Node(TestCase):

    def setUp(self):
        self.node = Schema__Html_Node()

    def test__init__(self):                                                     # Test basic initialization
        with self.node as _:
            assert type(_            ) is Schema__Html_Node
            assert type(_.attrs      ) is Type_Safe__Dict
            assert type(_.child_nodes) is Type_Safe__List
            assert type(_.text_nodes ) is Type_Safe__List
            assert type(_.tag        ) is str
            assert _.attrs             == {}
            assert _.child_nodes       == []
            assert _.text_nodes        == []
            assert _.tag               == ""
            assert _.position          == -1
            expected_json              =  { 'attrs'       : {}     ,
                                           'child_nodes' : []     ,
                                           'text_nodes'  : []     ,
                                           'tag'         : ''     ,
                                           'position'    : -1     }
            assert _.json()            == expected_json
            assert _.obj()             == __(attrs       = __()   ,
                                            child_nodes = []     ,
                                            text_nodes  = []     ,
                                            tag         = ''     ,
                                            position    = -1     )

    def test__init__with_params(self):                                         # Test initialization with parameters
        child_node = Schema__Html_Node(tag = 'span', position = 0)
        attrs_data = {'class': 'container', 'id': 'main'}
        node       = Schema__Html_Node(tag         = 'div'         ,
                                      attrs       = attrs_data     ,
                                      child_nodes = [child_node]   ,
                                      text_nodes  = []             ,
                                      position    = 1              )
        assert node.tag                         == 'div'
        assert node.attrs                       == attrs_data
        assert node.child_nodes                 == [child_node]
        assert len(node.child_nodes)            == 1
        assert type(node.child_nodes[0])        is Schema__Html_Node

    def test_nested_nodes(self):                                                # Test nested node structure
        grandchild_node = Schema__Html_Node(tag      = 'span'              ,
                                           position = 0                    )
        child_node      = Schema__Html_Node(tag         = 'div'            ,
                                           child_nodes = [grandchild_node] ,
                                           text_nodes  = []                ,
                                           position    = 0                 )
        parent_node     = Schema__Html_Node(tag         = 'article'        ,
                                           child_nodes = [child_node]      ,
                                           text_nodes  = []                ,
                                           position    = -1                )
        assert parent_node.child_nodes[0]                              == child_node
        assert parent_node.child_nodes[0].child_nodes[0]               == grandchild_node
        assert parent_node.child_nodes[0].child_nodes[0].tag           == 'span'

    def test_mixed_nodes(self):                                                 # Test mixed text and element nodes
        node_data   = Schema__Html_Node__Data(data     = 'Hello World'                         ,
                                             type     = Schema__Html_Node__Data__Type.TEXT    ,
                                             position = 0                                      )

        child_node  = Schema__Html_Node      (tag         = 'span'                             ,
                                             child_nodes = []                                  ,
                                             text_nodes  = []                                  ,
                                             position    = 1                                   )

        parent_node = Schema__Html_Node      (tag         = 'p'                                ,
                                             child_nodes = [child_node]                        ,
                                             text_nodes  = [node_data]                         ,
                                             position    = -1                                  )

        assert len(parent_node.child_nodes)       == 1
        assert len(parent_node.text_nodes)        == 1
        assert type(parent_node.text_nodes[0])    is Schema__Html_Node__Data
        assert type(parent_node.child_nodes[0])   is Schema__Html_Node
        assert parent_node.text_nodes[0].data     == 'Hello World'
        assert parent_node.child_nodes[0].tag     == 'span'