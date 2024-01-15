from osbot_utils.utils.Dev import pprint

from osbot_utils.base_classes.Kwargs_To_Self import Kwargs_To_Self
from osbot_utils.graphs.mem_graph.Mem_Graph import Mem_Graph
from osbot_utils.helpers.Print_Table import Print_Table


class Mem_Graph__Data(Kwargs_To_Self):

    mem_graph : Mem_Graph

    def edges(self):
        return self.mem_graph.edges

    def nodes(self):
        return self.mem_graph.nodes

    def nodes__by_key(self):
        by_key = {}
        for node in self.nodes():
            by_key[node.key] = node
        return by_key

    def nodes__keys(self):
        return [node.key for node in self.nodes()]

    def nodes_edges(self):
        nodes__edges = {}
        for node in self.nodes():
            nodes__edges[node.key] = []
        for edge in self.edges():
            nodes__edges[edge.from_node.key].append(edge.to_node.key)
        for node_key, edges_keys in nodes__edges.items():
            nodes__edges[node_key] = sorted(edges_keys)
        return nodes__edges

    def map_paths(self, key, paths, all_paths, nodes_edges):
        key_edges = nodes_edges[key]
        new_paths = []

        for edge_key in key_edges:
            for path in paths:
                if edge_key in path:
                    if path not in all_paths:
                        all_paths.append(path)
                else:
                    new_path = [*path, edge_key]
                    new_paths.append(new_path)
                    self.map_paths(edge_key, new_paths, all_paths, nodes_edges)
                    if new_path not in all_paths:
                        all_paths.append(new_path)
        # if new_paths:
        #     return new_paths

            # for edge_key in key_edges:
            #     self.map_paths(edge_key, paths, nodes_edges)
        return paths

    def nodes__find_all_paths(self):

        key         = self.nodes__keys()[0]
        nodes_edges = self.nodes_edges()
        #for key in self.nodes__keys():
        all_paths = []
        paths = [[key]]
        self.map_paths(key, paths,all_paths,  nodes_edges)
        pprint(all_paths)

    def print(self):
        with Print_Table() as _:
            _.set_title(self.mem_graph.config.graph_title)
            for node_key, edges_keys in self.nodes_edges().items():
                row = {'key': node_key,  'edges': edges_keys}
                _.add_data(row)
            _.set_order('key', 'edges')
            _.print()

    def print_adjacency_matrix(self):
        adjacency_matrix = self.nodes_edges__adjacency_matrix()
        node_keys        = sorted(self.nodes__keys())
        with Print_Table() as _:
            for row in adjacency_matrix:
                _.add_data(row)
            _.set_order('key', *node_keys)
            _.print()


    def node_edges__to_from(self):
        # Initialize a dictionary to hold the edges to and from for each node
        node_connections = { node_key: {'edges_to': [], 'edges_from': []} for node_key in self.nodes_edges().keys() }


        for node_key, edges_keys in self.nodes_edges().items():                 # Fill 'edges_to' and 'edges_from' for each node
            node_connections[node_key]['edges_from'].extend(edges_keys)         # 'edges_from' are the outgoing edges from 'node_key'

            for edge_key in edges_keys:                                         # 'edges_to' are the incoming edges to the nodes in 'edges_keys'
                if edge_key in node_connections:                                # Check if the edge_key represents a valid node
                    node_connections[edge_key]['edges_to'].append(node_key)

        return node_connections

    def nodes_edges__adjacency_matrix(self):
        nodes_edges = self.nodes_edges()                                                    # Retrieve the nodes and their edges
        node_keys = sorted(nodes_edges.keys())                                              # Get a sorted list of unique node keys
        node_indices = {node_key: index for index, node_key in enumerate(node_keys)}        # Create a mapping of node keys to their respective indices
        size = len(node_keys)                                                               # Initialize a square matrix with empty strings
        matrix = [['' for _ in range(size)] for _ in range(size)]

        for node_key, edges_keys in nodes_edges.items():                                    # Fill the matrix with 'X' if there is an edge between two nodes
            for edge_key in edges_keys:                                                     # Find the matrix positions based on node indices
                row_index = node_indices[node_key]
                col_index = node_indices[edge_key]
                matrix[row_index][col_index] = 'X'

        table_data = []
        for i, row in enumerate(matrix):
            row_data = {'key': node_keys[i]}
            row_data.update({node_keys[j]: row[j] for j in range(size)})
            table_data.append(row_data)
        return table_data

