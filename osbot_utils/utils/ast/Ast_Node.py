import ast
from osbot_utils.utils.Objects              import type_base_classes, obj_info, obj_data
from osbot_utils.utils.ast.Ast_Node_Registry import ast_node_registry


class Ast_Node:

    def __init__(self, node):
        if node.__module__ != 'ast':
             raise Exception(f'Expected node.__module__ to be ast, got: {node.__module__}')
        self.node      = node
        self.type      = node.__class__
        self.type_name = node.__class__.__name__

    def __repr__(self):
        return f"[Ast_Node][????] {self.type}"

    def ast_node(self, node):

        from osbot_utils.utils.ast.Ast_Argument     import Ast_Argument
        from osbot_utils.utils.ast.Ast_Arguments    import Ast_Arguments
        from osbot_utils.utils.ast.Ast_Constant     import Ast_Constant
        from osbot_utils.utils.ast.Ast_Function_Def import Ast_Function_Def
        from osbot_utils.utils.ast.Ast_Module       import Ast_Module
        from osbot_utils.utils.ast.Ast_Return       import Ast_Return
        node_type = type(node)

        if node_type is ast.arguments  : return Ast_Arguments   (node)
        if node_type is ast.arg        : return Ast_Argument    (node)
        if node_type is ast.Constant   : return Ast_Constant    (node)
        if node_type is ast.FunctionDef: return Ast_Function_Def(node)
        if node_type is ast.Module     :
            #resolved_type = ast_node_registry.resolve_type(ast.Module)
            #return resolved_type(node)
            return Ast_Module      (node)
        if node_type is ast.Return     : return Ast_Return      (node)

        return Ast_Node(node)
    def info(self):
        return obj_data(self.node)

    def source_code(self):
        return ast.unparse(self.node)

