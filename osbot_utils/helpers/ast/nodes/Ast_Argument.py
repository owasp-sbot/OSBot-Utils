from osbot_utils.helpers.ast.Ast_Node import Ast_Node


class Ast_Argument(Ast_Node):

    def info(self):
        return {'Ast_Argument': {'arg': self.node.arg}}