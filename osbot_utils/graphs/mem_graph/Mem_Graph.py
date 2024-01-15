from osbot_utils.utils.Misc import random_text

from osbot_utils.utils.Dev import pprint

from osbot_utils.utils.Files import pickle_save_to_file

from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.graphs.mem_graph.Mem_Graph__Config import Mem_Graph__Config
from osbot_utils.graphs.mem_graph.Mem_Graph__Edge    import Mem_Graph__Edge
from osbot_utils.graphs.mem_graph.Mem_Graph__Node    import Mem_Graph__Node



class Mem_Graph(Kwargs_To_Self):

    config : Mem_Graph__Config
    edges  : list[Mem_Graph__Edge]
    key    : str = random_text("mgraph")
    nodes  : list[Mem_Graph__Node]


    def __init__(self, **kwargs):
        super().__init__(**kwargs)

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

    # def save(self, format='pickle'):
    #     if format == 'pickle':
    #         return pickle_save_to_file(self)

    def save(self):
        from osbot_utils.graphs.mem_graph.Mem_Graph__Serializer import Mem_Graph__Serializer        # due to circular dependency
        return Mem_Graph__Serializer(mgraph=self).save()

    def print(self):
        print()
        return self.data().print()