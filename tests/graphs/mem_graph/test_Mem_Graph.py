from unittest                               import TestCase
from osbot_utils.utils.Misc                 import random_text
from osbot_utils.graphs.mem_graph.Mem_Graph import Mem_Graph


class test_Mem_Graph(TestCase):

    def setUp(self):
        self.mgraph = Mem_Graph()

    def test___init__(self):
        expected_args = ['config', 'edges', 'key', 'nodes']
        with self.mgraph as _:
            assert _.__attr_names__() == expected_args
            assert _.edges            == []
            assert _.nodes            == []
            assert _.key.startswith('mgraph_')

    def test_add_node(self):
        label = random_text()
        with self.mgraph as _:
            new_node = _.add_node(label=label)
            assert _.nodes               == [new_node]
            assert new_node.label        == label
            assert new_node.__locals__() == {'data': {} , 'key': label, 'label': label}

    def test_add_edge(self):
        label_1 = random_text()
        label_2 = random_text()
        with self.mgraph as _:
            from_node  = _.add_node(label=label_1)
            to_node    = _.add_node(label=label_2)
            new_edge   = _.add_edge(from_node=from_node, to_node=to_node)
            assert _.edges               == [new_edge]
            assert new_edge.from_node    == from_node
            assert new_edge.to_node      == to_node
            assert new_edge.__locals__() == {'data': {}, 'from_node': from_node, 'label':'', 'to_node': to_node}