from osbot_utils.graphs.mgraph.MGraph__Node import MGraph__Node


class Mermaid__Node(MGraph__Node):

    def __init__(self, node=None):
        super().__init__()
        if node:
            self.__dict__ = node.__dict__
        else:
            self.__dict__ = MGraph__Node().__dict__

    def code(self):
        label = self.label if self.label else self.key          # If label is not set, use key as label
        return f'  {self.key}["{label}"]'