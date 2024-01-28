from unittest import TestCase

from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Misc import list_set

from osbot_utils.graphs.mermaid.Mermaid__Node import Mermaid__Node


class test_Mermaid_Node(TestCase):

    def setUp(self):
        self.mermaid_node = Mermaid__Node()

    def test__init__(self):
        assert type(self.mermaid_node) is Mermaid__Node
        assert list_set(self.mermaid_node.__dict__) == ['attributes', 'key', 'label']

    # def test_code(self):
    #     with self.mermaid_node as _:
    #         assert _.code() == f'  {_.key}["{_.key}"]'
    #         assert _.label  == _.key
    #         _.label = 'my label'
    #         assert _.code() == f'  {_.key}["my label"]'

    def test_data(self):
        assert self.mermaid_node.data() == self.mermaid_node.__locals__()