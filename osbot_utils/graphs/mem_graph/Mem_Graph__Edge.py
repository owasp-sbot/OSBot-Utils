from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.graphs.mem_graph.Mem_Graph__Node   import Mem_Graph__Node


class Mem_Graph__Edge(Kwargs_To_Self):
    data      : dict
    from_node : Mem_Graph__Node
    label     : str
    to_node   : Mem_Graph__Node