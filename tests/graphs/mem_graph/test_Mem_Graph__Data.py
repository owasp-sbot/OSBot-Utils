from collections import defaultdict
from unittest import TestCase

from osbot_utils.utils.Misc import list_set

from osbot_utils.utils.Dev import pprint

from osbot_utils.graphs.mem_graph.Mem_Graph__Random_Graphs import Mem_Graph__Random_Graphs


class test_Mem_Graph__Data(TestCase):

    def setUp(self):
        self.graph      = Mem_Graph__Random_Graphs().with_x_nodes_and_y_edges(x=4,y=20)
        self.graph_data = self.graph.data()

    def test___init__(self):
        assert self.graph_data.__class__.__name__ == 'Mem_Graph__Data'
        assert self.graph_data.mem_graph == self.graph
        assert self.graph_data.nodes()   == self.graph.nodes
        assert self.graph_data.edges()   == self.graph.edges

    def test_nodes__edges(self):
        with self.graph_data as _:                                          # Use graph_data in a context manager
            nodes_edges = _.nodes_edges()                                   # Retrieve nodes and their edges
            assert list_set(nodes_edges) == _.nodes_keys()                  # Assert equality of nodes_edges and nodes_keys

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

    def test_print(self):
        #pprint(self.graph_data.nodes_edges())
        self.graph_data.print()

    def test_node_edges__to_from(self):
        self.graph_data.print_adjacency_matrix()
        #nodes_connections = self.graph_data.node_edges__to_from()
        #pprint(nodes_connections)


