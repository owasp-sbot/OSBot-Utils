from osbot_utils.graphs.mgraph.MGraph__Node import MGraph__Node
from osbot_utils.utils.Str import safe_str


class Mermaid__Node(MGraph__Node):

    # def __init__(self, node=None):
    #     super().__init__()
    #     if node:
    #         self.__dict__ = node.__dict__
    #     else:
    #         self.__dict__ = MGraph__Node().__dict__

    def cast(self, node):
        self.__dict__ = node.__dict__
        return self

    def code(self):
        label = self.label if self.label else self.key          # If label is not set, use key as label
        key = safe_str(self.key)
        return f'  {key}["{label}"]'