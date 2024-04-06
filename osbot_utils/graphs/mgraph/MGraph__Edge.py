from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.graphs.mermaid.Mermaid__Node import LINE_PADDING, Mermaid__Node
from osbot_utils.graphs.mgraph.MGraph__Node   import MGraph__Node
from osbot_utils.utils.Str import safe_str


class MGraph__Edge(Kwargs_To_Self):
    attributes : dict
    from_node  : MGraph__Node
    label      : str
    to_node    : MGraph__Node

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # def __repr__(self):
    #     return self.__str__()

    def __str__(self):
        return f'[Graph Edge] from "{self.from_node.key}" to "{self.to_node.key}" '

    # def cast(self, source):
    #     self.__dict__ = source.__dict__
    #     return self

    def data(self):
        return self.__locals__()             # todo: see if there is a better way to do this (specialy as the edge objects gets more features and attributes)
