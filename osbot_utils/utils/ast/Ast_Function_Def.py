from osbot_utils.utils.Objects           import obj_data
from osbot_utils.utils.ast.Ast_Arguments import Ast_Arguments
from osbot_utils.utils.ast.Ast_Node      import Ast_Node


class Ast_Function_Def(Ast_Node):

    def args(self):
        return Ast_Arguments(self.node.args)           # def convert to Ast_Arguments

    def __repr__(self):
        return f'[Ast_Node][Ast_Function_Def]'

    def info(self):
        return {'Ast_Function_Def': {'args'   : self.args().info(),
                                     'body'   : self.body()       ,
                                     'name'   : self.node.name    ,
                                     #'returns': self.returns()                 # this is for type hints
                                     }}

    def name(self):
        return self.node.name

