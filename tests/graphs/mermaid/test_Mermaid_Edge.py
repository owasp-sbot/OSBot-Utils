from unittest import TestCase
from osbot_utils.utils.Dev import pprint

from osbot_utils.graphs.mermaid.Mermaid__Node import Mermaid__Node
from osbot_utils.utils.Misc import list_set

from osbot_utils.graphs.mermaid.Mermaid__Edge import Mermaid__Edge


class test_Mermaid_Edge(TestCase):

    def setUp(self):
        self.mermaid_edge = Mermaid__Edge()

    def test__init__(self):
        assert type(self.mermaid_edge) is Mermaid__Edge
        assert list_set(self.mermaid_edge.__dict__) == ['attributes', 'from_node', 'label', 'to_node']

    # def test_code(self):
    #     from_node = self.mermaid_edge.from_node
    #     to_node   = self.mermaid_edge.to_node
    #     assert self.mermaid_edge.code() == f'{from_node.key} --> {to_node.key}'
    #     from_node.label = 'from node'
    #     to_node.label   = 'to node'
    #     assert self.mermaid_edge.code() == f'{from_node.key} --> {to_node.key}'
    #     self.mermaid_edge.label = 'link_type'
    #     assert self.mermaid_edge.code() == f'{from_node.key} --"{self.mermaid_edge.label}"--> {to_node.key}'
    #
    # def test_convert_nodes(self):
    #     assert type(self.mermaid_edge.from_node) is Mermaid__Node
    #     assert type(self.mermaid_edge.to_node  ) is Mermaid__Node