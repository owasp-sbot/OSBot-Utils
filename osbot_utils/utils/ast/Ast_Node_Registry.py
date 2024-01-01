

class Ast_Node_Registry:

    def __init__(self):
        self.node_types = {}

    def register_type(self, from_type, to_type):
        self.node_types[from_type] = to_type

    def resolve_type(self, type_name):
        return self.node_types.get(type_name)

    def ping(self):
        return 'pong'
ast_node_registry = Ast_Node_Registry()