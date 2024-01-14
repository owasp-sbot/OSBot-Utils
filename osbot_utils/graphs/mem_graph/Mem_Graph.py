from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.graphs.mem_graph.Mem_Graph__Config import Mem_Graph__Config
from osbot_utils.graphs.mem_graph.Mem_Graph__Edge    import Mem_Graph__Edge
from osbot_utils.graphs.mem_graph.Mem_Graph__Node    import Mem_Graph__Node



class Mem_Graph(Kwargs_To_Self):

    config : Mem_Graph__Config
    edges  : list[Mem_Graph__Edge]
    nodes  : list[Mem_Graph__Node]

    def add_edge(self, from_node, to_node):
        if self.config.allow_circle_edges is False:
            if from_node == to_node:
                return None
        if self.config.allow_duplicate_edges is False:                          # todo: figure out if there is a more efficient way to do this
            for edge in self.edges:
                if edge.from_node == from_node and edge.to_node == to_node:
                    return None
        new_edge = Mem_Graph__Edge(from_node=from_node, to_node=to_node)
        self.edges.append(new_edge)
        return new_edge

    def add_node(self, label):
        new_node = Mem_Graph__Node(label=label)
        self.nodes.append(new_node)
        return new_node

    def data(self):
        from osbot_utils.graphs.mem_graph.Mem_Graph__Data import Mem_Graph__Data
        return Mem_Graph__Data(mem_graph=self)
