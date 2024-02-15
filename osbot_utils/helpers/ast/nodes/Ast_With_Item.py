from osbot_utils.helpers.ast.Ast_Node import Ast_Node

class Ast_With_Item(Ast_Node):

    def info(self):
        return {'Ast_With_Item': {'context_expr' : self.context_expr()     ,
                                  'optional_vars': self.node.optional_vars}}