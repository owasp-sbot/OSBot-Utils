from osbot_utils.utils.Objects import obj_data


class Ast_Base:

    def __init__(self, node):
        if node.__module__ != 'ast':
             raise Exception(f'Expected node.__module__ to be ast, got: {node.__module__}')
        self.node      = node
        self._type      = node.__class__
        self._type_name = node.__class__.__name__

    def obj_data(self):
        return obj_data(self.node)