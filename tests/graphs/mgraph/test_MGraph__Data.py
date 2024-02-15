from collections import defaultdict
from unittest import TestCase

import pytest

from osbot_utils.graphs.mgraph.MGraph__Edge import MGraph__Edge
from osbot_utils.testing.Stdout import Stdout
from osbot_utils.utils.Misc import list_set

from osbot_utils.utils.Dev import pprint

from osbot_utils.graphs.mgraph.MGraph__Random_Graphs import MGraph__Random_Graphs


class test_MGraph__Data(TestCase):

    def setUp(self):
        self.x          = 5
        self.y          = 10
        self.mgraph     = MGraph__Random_Graphs().with_x_nodes_and_y_edges(x=self.x, y=self.y)
        self.graph_data = self.mgraph.data()

    def test___init__(self):
        assert self.graph_data.__class__.__name__ == 'MGraph__Data'
        assert self.graph_data.mgraph    == self.mgraph
        assert self.graph_data.nodes()   == self.mgraph.nodes
        assert self.graph_data.edges()   == self.mgraph.edges

    def test_nodes__edges(self):
        with self.graph_data as _:                                          # Use graph_data in a context manager
            nodes_edges = _.nodes_edges()                                   # Retrieve nodes and their edges
            assert list_set(nodes_edges) == sorted(_.nodes__keys())         # Assert equality of nodes_edges and nodes_keys

            expected_data = defaultdict(list)                               # Defaultdict for storing expected data
            for edge in _.edges():                                          # Iterate over all edges in the graph
                from_key = edge.from_node.key                               # Get key of the from_node
                to_key  = edge.to_node.key                                  # Get key of the to_node
                expected_data[from_key].append(to_key)                      # Append to_key to the list of from_key

            for node_key, nodes_edges_keys in expected_data.items():        # Iterate over expected data items
                assert nodes_edges[node_key] == sorted(nodes_edges_keys)    # Assert the node's edges match expected
                del nodes_edges[node_key]                                   # Remove node_key from nodes_edges after assertion
            for node_key, nodes_edges_keys in nodes_edges.items():          # Iterate over remaining items in nodes_edges
                assert nodes_edges_keys == []                               # Assert that no edges are left untested

    # todo: finish implementing method
    @pytest.mark.skip('finish implementing method')
    def test_nodes__find_all_paths(self):
        with self.graph_data as _:
            _.print()
            all_paths = _.nodes__find_all_paths()
            # for path in all_paths:
            #     print(path)
            #     print()

    def test_edges(self):
        with self.graph_data as _:
            for edge in _.edges():
                assert type(edge) is MGraph__Edge


    def test_print(self):
        with Stdout() as stdout:
            with self.graph_data as _:
                _.print()
        third_line = stdout.value().split('\n')[2]          # todo: improve this test
        assert 'key'   in third_line
        assert 'edges' in third_line


    def test_print_adjacency_matrix(self):
        with Stdout() as stdout:
             self.graph_data.print_adjacency_matrix()
        for node in self.graph_data.nodes():
            assert node.key in stdout.value()
        #pprint(stdout.value())                     # use this to see what the adjacency_matrix looks like



