from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Name(Ast_Node):

    def __repr__(self):
        return f'[Ast_Node][Ast_Name]'

    def info(self):
        return {'Ast_Name': {'ctx': self.ctx()}}