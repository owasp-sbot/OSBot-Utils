from unittest                                                             import TestCase
from osbot_utils.helpers.html.schemas.Schema__Html_Node                   import Schema__Html_Node
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data             import Schema__Html_Node__Data
from osbot_utils.helpers.html.schemas.Schema__Html_Node__Data__Type       import Schema__Html_Node__Data__Type
from osbot_utils.type_safe.Type_Safe__Dict                                import Type_Safe__Dict
from osbot_utils.type_safe.Type_Safe__List                                import Type_Safe__List
from osbot_utils.utils.Objects                                            import __

class test_Schema__Html_Node(TestCase):

    def setUp(self):
        self.node = Schema__Html_Node()

    def test__init__(self):
        with self.node as _:
            assert type(_       ) is Schema__Html_Node
            assert type(_.attrs ) is Type_Safe__Dict
            assert type(_.nodes ) is Type_Safe__List
            assert type(_.tag   ) is str
            assert _.attrs        == {}
            assert _.nodes        == []
            assert _.tag          == ""
            assert _.json()       == {'attrs': {}, 'nodes': [], 'tag': ''}
            assert _.obj ()       == __(attrs=__(), nodes=[], tag='')

    def test__init__with_params(self):
        child_node = Schema__Html_Node(tag='span')
        attrs_data = {'class': 'container', 'id': 'main'}
        node       = Schema__Html_Node(tag      = 'div'          ,
                                       attrs    = attrs_data     ,
                                       nodes    = [child_node   ])
        assert node.tag                  == 'div'
        assert node.attrs                == attrs_data
        assert node.nodes                == [child_node]
        assert len(node.nodes)           == 1
        assert type(node.nodes[0])       is Schema__Html_Node

    def test_nested_nodes(self):
        grandchild_node = Schema__Html_Node(tag='span')
        child_node      = Schema__Html_Node(tag     = 'div'                     ,
                                             nodes = [grandchild_node])
        parent_node     = Schema__Html_Node(tag    = 'article'                 ,
                                             nodes = [child_node   ])
        assert parent_node.nodes[0]              == child_node
        assert parent_node.nodes[0].nodes[0]     == grandchild_node
        assert parent_node.nodes[0].nodes[0].tag == 'span'

    def test_mixed_nodes(self):
        node_data    = Schema__Html_Node__Data(data='Hello World', type=Schema__Html_Node__Data__Type.TEXT)
        child_node   = Schema__Html_Node      (tag   ='span'                  )
        parent_node  = Schema__Html_Node      (tag   = 'p'                    ,
                                               nodes = [node_data, child_node ])
        assert len(parent_node.nodes)        == 2
        assert type(parent_node.nodes[0]) is Schema__Html_Node__Data
        assert type(parent_node.nodes[1])    is Schema__Html_Node
        assert parent_node.nodes[0].data     == 'Hello World'
        assert parent_node.nodes[1].tag      == 'span'