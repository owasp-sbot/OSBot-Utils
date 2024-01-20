from osbot_utils.graphs.mgraph.views.mermaid.Mermaid_Node import Mermaid_Node
from osbot_utils.utils.Dev            import pprint
from osbot_utils.graphs.mgraph.MGraph import MGraph


class Mermaid_MGraph(MGraph):

    def __init__(self, mgraph=None):
        super().__init__()
        self.__dict__ = mgraph.__dict__
        self.convert_nodes()

    def code(self):
        return 'aaa'

    def convert_nodes(self):
        new_nodes = []
        for node in self.nodes:
            new_nodes.append(Mermaid_Node(node))
        self.nodes = new_nodes

    def print_2(self):
        pprint(self.data().graph_data())