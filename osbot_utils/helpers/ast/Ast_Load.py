import ast

from osbot_utils.helpers.Type_Registry  import type_registry
from osbot_utils.utils.Files            import file_contents, file_exists
from osbot_utils.utils.Functions        import python_file
from osbot_utils.helpers.ast.Ast_Node   import Ast_Node

#todo: check if this is still needed since it Ast_Visit does it similar
class Ast_Load(ast.NodeVisitor):

    def __init__(self):
        self.ast_nodes = {}
        self.files_visited = []

    def load_file(self, file_path):
        if file_exists(file_path):
            file_visited = "/".join(file_path.split('/')[-4:])
            source_code  = file_contents(file_path)
            tree         = ast.parse(source_code)
            self.visit(tree)
            self.files_visited.append(file_visited)
            return True
        return False

    def load_files(self, files_paths):
        for file_path in files_paths:
            self.load_file(file_path)

    def load_target(self, file_path):
        file = python_file(file_path)
        return self.load_file(file)

    def add_visited_node(self, node):
        ast_node     = self.create_ast_node(node)
        ast_node_key = ast_node.key()  #ast_node.__class__.__name__
        if self.ast_nodes.get(ast_node_key) is None:
            self.ast_nodes[ast_node_key] = []
        self.ast_nodes[ast_node_key].append(ast_node)

    def create_ast_node(self, node):
        type_key      = type(node)
        resolved_type = type_registry.resolve(type_key)
        if resolved_type:
           return resolved_type(node)
        return Ast_Node(node)

    def generic_visit(self, node):
        #print(f'entering {node.__class__.__name__}')
        self.add_visited_node(node)
        super().generic_visit(node)

    def stats(self):
        nodes = {}
        node_count = 0
        for key,list in self.ast_nodes.items():
            key_count = len(list)
            nodes[key] = key_count
            node_count += key_count
        stats = { 'files_visited': self.files_visited,
                  'node_count' : node_count,
                  'nodes'      : nodes    }
        return stats
