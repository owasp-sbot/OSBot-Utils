from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self

from osbot_utils.graphs.mgraph.MGraph import MGraph
from osbot_utils.graphs.mgraph.MGraph__Config import MGraph__Config
from osbot_utils.utils.Misc import random_int


class MGraph__Random_Graphs(Kwargs_To_Self):
    config     : MGraph__Config
    graph_key : str

    def new_graph(self):
        return MGraph(config=self.config, key=self.graph_key)

    def with_x_nodes_and_y_edges(self, x=10, y=20):
        MGraph = self.new_graph()
        if x >0  and y > 0 :
            for i in range(x):
                MGraph.add_node(label=f'node_{i}')
            for i in range(y):
                from_node_id = random_int(max=x) - 1
                to_node_id   = random_int(max=x) - 1
                from_node    = MGraph.nodes[from_node_id]
                to_node      = MGraph.nodes[to_node_id  ]
                MGraph.add_edge(from_node=from_node, to_node=to_node)

        return MGraph