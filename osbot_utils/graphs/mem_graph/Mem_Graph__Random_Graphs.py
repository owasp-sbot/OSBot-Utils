from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

from osbot_utils.graphs.mem_graph.Mem_Graph import Mem_Graph
from osbot_utils.graphs.mem_graph.Mem_Graph__Config import Mem_Graph__Config
from osbot_utils.utils.Misc import random_int


class Mem_Graph__Random_Graphs(Kwargs_To_Self):
    config : Mem_Graph__Config

    def new_graph(self):
        return Mem_Graph(config=self.config)

    def with_x_nodes_and_y_edges(self, x=10, y=20):
        mem_graph = self.new_graph()
        if x >0  and y > 0 :
            for i in range(x):
                mem_graph.add_node(label=f'node_{i}')
            for i in range(y):
                from_node_id = random_int(max=x) - 1
                to_node_id   = random_int(max=x) - 1
                from_node    = mem_graph.nodes[from_node_id]
                to_node      = mem_graph.nodes[to_node_id  ]
                mem_graph.add_edge(from_node=from_node, to_node=to_node)

        return mem_graph