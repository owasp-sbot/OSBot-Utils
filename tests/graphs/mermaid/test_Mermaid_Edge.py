from unittest import TestCase

from osbot_utils.graphs.mermaid.Mermaid import Mermaid
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

    def test__config__edge__output_node_from(self):
        with Mermaid() as _:
            new_edge = _.add_edge('id', 'id2').output_node_from()
            assert _.code()               == 'graph LR\n    id["id"]\n    id2["id2"]\n\n    id["id"] --> id2'
            assert new_edge.config.output_node_from is True
            assert new_edge.render_edge() == '    id["id"] --> id2'
            new_edge.output_node_from(False)
            assert new_edge.config.output_node_from is False
            assert new_edge.render_edge() == '    id --> id2'