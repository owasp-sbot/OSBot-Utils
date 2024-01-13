from osbot_utils.helpers.ast            import Ast_Module
from osbot_utils.helpers.ast.Ast_Base   import Ast_Base

class Ast_Visit:

    def __init__(self, target):
        if isinstance(target, Ast_Base):                    # support when we pass an Ast_Node
            self.ast_node = target
        else:
            self.ast_node = Ast_Module(target)                # or when we pass source code, or a python object
        self.node_handlers    = {}
        self.capture_handlers = {}

    def __enter__(self): return self
    def __exit__(self, exc_type, exc_val, exc_tb): pass

    def capture(self, node_type, callback):
        self.capture_handlers[node_type] = { 'callback': callback,
                                             'nodes'   : []      }
        return self

    def capture_calls(self, callback=None):
        return self.capture('Ast_Call', callback)

    def capture_imports(self, callback=None):
        self.capture('Ast_Import'     , callback)
        self.capture('Ast_Import_From', callback)
        return self

    def capture_modules(self, callback=None):
        return self.capture('Ast_Module', callback)

    def capture_functions(self, callback=None):
        return self.capture('Ast_Function_Def', callback)

    def captured_nodes(self):
        captured = {}
        for node_type, data in self.capture_handlers.items():
            captured[node_type] = data['nodes']
        return captured

    def invoke_capture_callbacks(self):
        for node_type, data in self.capture_handlers.items():
            callback = data['callback']
            nodes    = data['nodes']
            if callback:
                callback(nodes)

    def on_node(self, node):
        node_type = type(node).__name__
        if node_type in self.capture_handlers:
            self.capture_handlers[node_type]['nodes'].append(node)
        if node_type in self.node_handlers:
            for handler in self.node_handlers[node_type]:
                handler(node)

    def stats(self):
        stats = {}
        for node_type, data in self.capture_handlers.items():
            stats[node_type] = len(data['nodes'])
        return stats

    def register_node_handler(self, node_type, handler):
        if node_type not in self.node_handlers:
            self.node_handlers[node_type] = []
        self.node_handlers[node_type].append(handler)
        return self

    def visit(self):
        self.visit_node(self.ast_node)
        self.invoke_capture_callbacks()
        return self

    def visit_node(self, node):
        if isinstance(node, Ast_Base):
            self.on_node(node)
            self.visit_node(node.info())
        elif type(node) is dict:
            for _, value in node.items():
                self.visit_node(value)
        elif type(node) is list:
            for item in node:
                self.visit_node(item)


