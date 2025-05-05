from unittest                                                             import TestCase
from osbot_utils.helpers.html.schemas.Schema__HTML_Node                   import Schema__HTML_Node
from osbot_utils.helpers.html.schemas.Schema__HTML_Node__Data             import Schema__HTML_Node__Data
from osbot_utils.helpers.html.schemas.Schema__HTML_Node__Data__Type       import Schema__HTML_Node__Data__Type
from osbot_utils.type_safe.Type_Safe__Dict                                import Type_Safe__Dict
from osbot_utils.type_safe.Type_Safe__List                                import Type_Safe__List
from osbot_utils.utils.Objects                                            import __

class test_Schema__HTML_Node(TestCase):

    def setUp(self):
        self.node = Schema__HTML_Node()

    def test__init__(self):
        with self.node as _:
            assert type(_       )           is Schema__HTML_Node
            assert type(_.attrs )           is Type_Safe__Dict
            assert type(_.children)         is Type_Safe__List
            assert type(_.tag   )           is str
            assert _.attrs                  == {}
            assert _.children               == []
            assert _.tag                    == ""
            assert _.json()                 == {'attrs': {}, 'children': [], 'tag': ''}
            assert _.obj ()                 == __(attrs=__(), children=[], tag='')

    def test__init__with_params(self):
        child_node = Schema__HTML_Node(tag='span')
        attrs_data = {'class': 'container', 'id': 'main'}
        node       = Schema__HTML_Node(tag      = 'div'          ,
                                       attrs    = attrs_data     ,
                                       children = [child_node   ])
        assert node.tag                     == 'div'
        assert node.attrs                   == attrs_data
        assert node.children                == [child_node]
        assert len(node.children)           == 1
        assert type(node.children[0])       is Schema__HTML_Node

    def test_nested_nodes(self):
        grandchild_node = Schema__HTML_Node(tag='span')
        child_node      = Schema__HTML_Node(tag       = 'div'                     ,
                                             children = [grandchild_node])
        parent_node     = Schema__HTML_Node(tag       = 'article'                 ,
                                             children = [child_node   ])
        assert parent_node.children[0]                      == child_node
        assert parent_node.children[0].children[0]          == grandchild_node
        assert parent_node.children[0].children[0].tag      == 'span'

    def test_mixed_children(self):
        node_data    = Schema__HTML_Node__Data(data='Hello World', type=Schema__HTML_Node__Data__Type.TEXT)
        child_node   = Schema__HTML_Node      (tag       ='span'                  )
        parent_node  = Schema__HTML_Node      (tag       = 'p'                    ,
                                                children = [node_data, child_node ])
        assert len(parent_node.children)        == 2
        assert type(parent_node.children[0])    is Schema__HTML_Node__Data
        assert type(parent_node.children[1])    is Schema__HTML_Node
        assert parent_node.children[0].data     == 'Hello World'
        assert parent_node.children[1].tag      == 'span'