from unittest import TestCase

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.graphs.mermaid.Mermaid import Mermaid
from osbot_utils.graphs.mgraph.MGraph__Node import MGraph__Node
from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Misc import list_set

from osbot_utils.graphs.mermaid.Mermaid__Node import Mermaid__Node
from osbot_utils.utils.Objects import type_mro


class test_Mermaid_Node(TestCase):

    def setUp(self):
        self.mermaid_node = Mermaid__Node()
        self.node_config  = self.mermaid_node.config

    def test__init__(self):
        assert type(self.mermaid_node) is Mermaid__Node
        assert list_set(self.mermaid_node.__dict__) == ['attributes', 'config', 'key', 'label']

    # def test_code(self):
    #     with self.mermaid_node as _:
    #         assert _.code() == f'  {_.key}["{_.key}"]'
    #         assert _.label  == _.key
    #         _.label = 'my label'
    #         assert _.code() == f'  {_.key}["my label"]'

    def test_data(self):
        assert self.mermaid_node.data() == self.mermaid_node.__locals__()

    def test_wrap_with_quotes(self):

        assert self.node_config.wrap_with_quotes                                 == True
        assert self.mermaid_node.wrap_with_quotes(     ).config.wrap_with_quotes == True
        assert self.mermaid_node.wrap_with_quotes(False).config.wrap_with_quotes == False
        assert self.mermaid_node.wrap_with_quotes(True ).config.wrap_with_quotes == True

    def test__config__wrap_with_quotes(self):
        new_node = self.mermaid_node.set_key('id').set_label('id')
        new_node.wrap_with_quotes()
        assert type(new_node) is Mermaid__Node
        assert new_node.config.wrap_with_quotes == True
        assert new_node.key == 'id'

        assert new_node.data() == {'attributes' : {}                        ,
                                   'config'     : new_node.config           ,
                                   'key'        : 'id'                      ,
                                   'label'      : 'id'                      }
        assert type_mro(new_node) == [Mermaid__Node, MGraph__Node, Kwargs_To_Self, object]

        with Mermaid() as _:
            _.add_node(key='id')
            assert _.code() == 'graph LR\n    id["id"]\n'
        with Mermaid() as _:
            _.add_node(key='id').wrap_with_quotes(False)
            assert _.code() == 'graph LR\n    id[id]\n'

        mermaid = Mermaid()
        new_node = mermaid.add_node(key='id')
        new_node.wrap_with_quotes(False)
        assert type(new_node) == Mermaid__Node
        assert new_node.attributes == {}
        assert mermaid.code() == 'graph LR\n    id[id]\n'

