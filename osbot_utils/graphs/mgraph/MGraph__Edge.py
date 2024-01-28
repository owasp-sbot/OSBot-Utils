from osbot_utils.base_classes.Kwargs_To_Self        import Kwargs_To_Self
from osbot_utils.graphs.mermaid.Mermaid__Node import LINE_PADDING, Mermaid__Node
from osbot_utils.graphs.mgraph.MGraph__Node   import MGraph__Node
from osbot_utils.utils.Str import safe_str


class MGraph__Edge(Kwargs_To_Self):
    attributes : dict
    from_node  : Mermaid__Node
    label      : str
    to_node    : Mermaid__Node

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'[Graph Edge] from "{self.from_node.key}" to "{self.to_node.key}" '

    def cast(self, source):
        self.__dict__ = source.__dict__
        return self

    def data(self):
        return self.__locals__()             # todo: see if there is a better way to do this (specialy as the edge objects gets more features and attributes)

    def render_edge(self):
        from_node_key = safe_str(self.from_node.key)
        to_node_key   = safe_str(self.to_node  .key)
        if self.attributes.get('output_node_from'):
            from_node_key =  self.from_node.render_node(include_padding=False) #f'{edge.from_node.key}["{edge.from_node.label}"]'
        if self.attributes.get('output_node_to'):
            to_node_key   = self.to_node.render_node(include_padding=False   ) #f'{edge.to_node  .key}["{edge.to_node  .label}"]'
        if self.attributes.get('edge_mode') == 'lr_using_pipe':
            link_code      = f'-->|{self.label}|'
        elif self.label:
            link_code      = f'--"{self.label}"-->'
        else:
            link_code      = '-->'
        edge_code      = f'{LINE_PADDING}{from_node_key} {link_code} {to_node_key}'
        return edge_code