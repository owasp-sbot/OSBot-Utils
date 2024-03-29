from osbot_utils.utils.Misc import random_text, lower
from osbot_utils.base_classes.Kwargs_To_Self   import Kwargs_To_Self
from osbot_utils.graphs.mgraph.MGraph__Config  import MGraph__Config
from osbot_utils.graphs.mgraph.MGraph__Edge    import MGraph__Edge
from osbot_utils.graphs.mgraph.MGraph__Node    import MGraph__Node



class MGraph(Kwargs_To_Self):

    config : MGraph__Config
    edges  : list[MGraph__Edge]
    key    : str
    nodes  : list[MGraph__Node]


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.key:
            self.key = random_text("mgraph", lowercase=True)                 # make sure there is always a key

    def add_edge(self, from_node, to_node, label=None,attributes=None):
        if self.config.allow_circle_edges is False:
            if from_node == to_node:
                return None
        if self.config.allow_duplicate_edges is False:                          # todo: figure out if there is a more efficient way to do this
            for edge in self.edges:
                if edge.from_node == from_node and edge.to_node == to_node:
                    return None
        new_edge = MGraph__Edge(from_node=from_node, to_node=to_node, label=label, attributes=attributes)
        self.edges.append(new_edge)
        return new_edge

    def add_node(self, key=None, label=None, attributes=None):
        new_node = MGraph__Node(key=key, label=label, attributes=attributes)
        self.nodes.append(new_node)
        return new_node

    def data(self):
        from osbot_utils.graphs.mgraph.MGraph__Data import MGraph__Data
        return MGraph__Data(mgraph=self)

    # def save(self, format='pickle'):
    #     if format == 'pickle':
    #         return pickle_save_to_file(self)

    def save(self):
        from osbot_utils.graphs.mgraph.MGraph__Serializer import MGraph__Serializer        # due to circular dependency
        return MGraph__Serializer(mgraph=self).save()

    def print(self):
        print()
        return self.data().print()