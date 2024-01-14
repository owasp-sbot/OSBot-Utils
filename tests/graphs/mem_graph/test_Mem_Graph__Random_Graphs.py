from unittest                                               import TestCase
from osbot_utils.graphs.mem_graph.Mem_Graph__Random_Graphs  import Mem_Graph__Random_Graphs
from osbot_utils.utils.Misc                                 import random_int


class test_Mem_Graph__Random_Graphs(TestCase):

    def setUp(self):
        self.ramdom_graphs = Mem_Graph__Random_Graphs()
        self.config        = self.ramdom_graphs.config

    def test_with_x_nodes_and_y_edges(self):
        print()
        self.config.allow_circle_edges    = True            # need to set this or the test below will fail
        self.config.allow_duplicate_edges = True
        x = random_int(max=10)
        y = random_int(max=20)
        new_graph = self.ramdom_graphs.with_x_nodes_and_y_edges(x, y)
        assert type(new_graph).__name__ == 'Mem_Graph'
        assert len(new_graph.nodes)    == x
        assert len(new_graph.edges)    == y