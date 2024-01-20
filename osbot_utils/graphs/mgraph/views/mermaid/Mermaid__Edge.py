from osbot_utils.graphs.mgraph.MGraph__Edge import MGraph__Edge
from osbot_utils.graphs.mgraph.views.mermaid.Mermaid__Node import Mermaid__Node
from osbot_utils.utils.Str import safe_str


class Mermaid__Edge(MGraph__Edge):
    from_node : Mermaid__Node
    to_node   : Mermaid__Node

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.convert_nodes()

    def cast(self, edge):
        self.__dict__ = edge.__dict__
        self.convert_nodes()
        return self

    def code(self):
        from_node_key = safe_str(self.from_node.key)
        to_node_key   = safe_str(self.to_node.key)
        if self.label:
            link_code      = f'--"{self.label}"-->'
        else:
            link_code      = '-->'
        edge_code      = f'{from_node_key} {link_code} {to_node_key}'
        return edge_code

    def convert_nodes(self):
        self.from_node = Mermaid__Node().cast(self.from_node)
        self.to_node   = Mermaid__Node().cast(self.to_node  )