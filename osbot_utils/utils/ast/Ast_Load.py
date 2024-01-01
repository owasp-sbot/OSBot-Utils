from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Load(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Load]'

    def info(self):
        #self.print()
        return {'Ast_Load': {}}