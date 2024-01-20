from osbot_utils.graphs.mgraph.views.mermaid.Mermaid_Node import Mermaid_Node
from osbot_utils.utils.Dev            import pprint
from osbot_utils.graphs.mgraph.MGraph import MGraph


class Mermaid_MGraph(MGraph):

    nodes       : list[Mermaid_Node]

    def __init__(self, mgraph=None):
        super().__init__()
        self.__dict__ = mgraph.__dict__
        self.convert_nodes()
        self.mermaid_code = []

    def add_line(self, line):
        self.mermaid_code.append(line)
        return line

    def code(self):
        self.code_create()
        return '\n'.join(self.mermaid_code)

    def code_create(self):
        with self as _:
            _.reset_code()
            _.add_line('graph TB')
            for node in _.nodes:
                _.add_line(node.code())
        return self

    def code_markdown(self):
        self.code_create()
        markdown = ['# Mermaid Graph',
                    "```mermaid" ,
                    *self.mermaid_code,
                    "```"]

        return '\n'.join(markdown)

    def convert_nodes(self):
        new_nodes = []
        for node in self.nodes:
            new_nodes.append(Mermaid_Node(node))
        self.nodes = new_nodes

    def reset_code(self):
        self.mermaid_code = []
        return self

    def save(self):
        file_path = '/tmp/mermaid.md'

        with open(file_path, 'w') as file:
            file.write(self.code_markdown())
        return file_path
