from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.graphs.mem_graph.Mem_Graph__Node   import Mem_Graph__Node


class Mem_Graph__Edge(Kwargs_To_Self):
    data      : dict
    from_node : Mem_Graph__Node
    label     : str
    to_node   : Mem_Graph__Node

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'[Graph Edge] from "{self.from_node.key}" to "{self.to_node.key}" '