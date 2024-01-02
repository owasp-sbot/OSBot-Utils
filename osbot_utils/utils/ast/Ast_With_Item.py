from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_With_Item(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_With_Item]'

    def info(self):
        return {'Ast_With_Item': {'context_expr' : self.context_expr()     ,
                                  'optional_vars': self.node.optional_vars}}