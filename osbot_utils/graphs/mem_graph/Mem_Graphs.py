import random

from osbot_utils.utils.Files import file_exists, file_extension, pickle_load_from_file

from osbot_utils.graphs.mem_graph.Mem_Graph__Random_Graphs import Mem_Graph__Random_Graphs


class Mem_Graphs:

    def new__random(self, config=None):
        return Mem_Graph__Random_Graphs(config=config).with_x_nodes_and_y_edges()

    def load(self, file_path):
        if file_exists(file_path):
            if file_extension(file_path):
                return pickle_load_from_file(file_path)