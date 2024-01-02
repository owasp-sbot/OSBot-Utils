from osbot_utils.utils.ast.Ast_Node import Ast_Node

class Ast_Name(Ast_Node):

    def info(self):
        return {'Ast_Name': {'ctx': self.ctx()}, 'id': self.id() }